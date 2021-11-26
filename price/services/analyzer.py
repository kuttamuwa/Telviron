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
    :param kwargs:
    timeframe: 1h, 1w, 1d, 1m etc.
    since: Format %Y-%m-%dT%H:%M:%S
    limit: default 1000

    :return:
    """
    yesterday = kwargs.get('since', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'))
    yesterday = exchange.parse8601(yesterday)

    asset_data = exchange.fetch_ohlcv(symbol, timeframe=kwargs.get('timeframe', '1h'),
                                      since=yesterday, limit=kwargs.get('limit'))
    asset_data = asset_df(asset_data)

    return asset_data


def ovhl_htf(symbol):
    """

    :param symbol:
    :return:
    """
    data_periods = {

    }
    data = exchange.fetch_ohlcv(symbol, limit=365, timeframe="1d")  # daily whole year
    data = asset_df(data)

    # current monthly
    cmo = data[(data['Timestamp'].dt.month == datetime.now().month) & (data['Timestamp'].dt.day == 1)]
    data_periods['Monthly'] = cmo

    # previous month
    pmo = data[(data['Timestamp'].dt.month == datetime.now().month - 1) & (data['Timestamp'].dt.day == 1)]
    data_periods['Previous Month'] = pmo

    # yearly
    yo = data[(data['Timestamp'].dt.year == datetime.now().year) & (data['Timestamp'].dt.day == 1) & (
            data['Timestamp'].dt.month == 1)]
    data_periods['Yearly'] = yo

    # previous week
    pwo = data[(data['Timestamp'].dt.day_of_week == 0) & (data['Timestamp'].dt.day == 1)].iloc[-1]
    data_periods['Previous Week'] = pwo

    # daily
    do = data.iloc[-1]
    data_periods['Daily'] = do

    # previous day open
    pdo = data.iloc[-2]
    data_periods['Previous Day'] = pdo

    return data_periods


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
        data_periods[f"EMA_{p}"] = ema_level

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


def ma_ribbons(symbol, timeframe, source='Close', periods=(20, 50, 100, 200, 400)):
    data_periods = {

    }
    for p in periods:
        data = exchange.fetch_ohlcv(symbol, limit=p, timeframe=timeframe)
        data = asset_df(data)

        sma_level = talib.SMA(data[source], timeperiod=p)
        data_periods[f"SMA_{p}"] = sma_level

    return data_periods
