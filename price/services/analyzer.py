from datetime import timedelta, datetime

import ccxt
import pandas as pd
import talib
from celery import shared_task

# only exchange for now
exchange = ccxt.binance()


def asset_df(asset_data) -> pd.DataFrame:
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    asset_data = pd.DataFrame(asset_data, columns=header)
    asset_data['Timestamp'] = [datetime.utcfromtimestamp(i // 1000) for i in asset_data.Timestamp]

    return asset_data


@shared_task
def ovhl_hourly_since_yesterday(symbol, **kwargs):
    """
    Default latest 24 hour whole data per hour timeframe
    :param symbol: BTC/USDT
    :return:
    """
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%dT%H:%M:%S')
    yesterday = exchange.parse8601(yesterday)

    timeframe = kwargs.get('timeframe', '1h')

    asset_data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=yesterday)
    asset_data = asset_df(asset_data)

    return asset_data


def ema_ribbons(symbol, timeframe, source='Close', periods=(20, 50, 100, 200, 400)):
    """
    Calculate EMA levels.

    EMA200:
    Solution1:    data['EMA'] = data['Close'].rolling(200).mean().dropna()

    Solution2:    ema200 = talib.EMA(data.Close, timeperiod=200)

    :param symbol:
    :param timeframe:
    :param source:
    :param periods:
    :return:
    """
    data_periods = {

    }
    for p in periods:
        data = exchange.fetch_ohlcv(symbol, limit=p, timeframe=timeframe)
        data = asset_df(data)

        ema_level = talib.EMA(data[source], timeperiod=p)
        data_periods[f"EMA{p}"] = ema_level

    return data_periods


def bollinger_bands(symbol, timeframe, source='Close', periods=(20, 50, 100, 200, 400)):
    data_periods = {

    }
    for p in periods:
        data = exchange.fetch_ohlcv(symbol, limit=p, timeframe=timeframe)
        data = asset_df(data)

        data_series = data[source]
        up, mid, low = talib.BBANDS(data_series, timeperiod=p)
        up, mid, low = up.iloc[-1], mid.iloc[-1], low.iloc[-1]

        data_periods[f'Bollinger{p}'] = {
            'up': up,
            'mid': mid,
            'low': low
        }
