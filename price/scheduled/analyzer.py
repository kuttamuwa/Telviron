from datetime import timedelta, datetime

import ccxt
import pandas as pd
import talib
from celery import shared_task
# only exchange for now
from django_celery_beat.models import PeriodicTask

from notifications.models.models import TelegramActive
from notifications.services.telegram.ITelegram import TelegramDataService

exchange = ccxt.binance()


def asset_df(asset_data) -> pd.DataFrame:
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    asset_data = pd.DataFrame(asset_data, columns=header)
    asset_data['Timestamp'] = [datetime.utcfromtimestamp(i // 1000) for i in asset_data.Timestamp]

    return asset_data


series_to_json = lambda x: f"Open : {float(x['Open'])} \n " \
                           f"High : {float(x['High'])} \n" \
                           f"Low : {float(x['Low'])} \n " \
                           f"Close : {float(x['Close'])} \n " \
                           f"Volume : {float(x['Volume'])}"


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


@shared_task
def ovhl_htf(symbol):
    """

    :param symbol:
    :return:
    """
    data_periods = {
        'symbol': symbol
    }

    data = exchange.fetch_ohlcv(symbol, limit=365, timeframe="1d")  # daily whole year
    data = asset_df(data)

    # current monthly
    cmo = data[(data['Timestamp'].dt.month == datetime.now().month) & (data['Timestamp'].dt.day == 1)]
    data_periods['Monthly'] = series_to_json(cmo.drop(columns=['Timestamp']))

    # previous month
    pmo = data[(data['Timestamp'].dt.month == datetime.now().month - 1) & (data['Timestamp'].dt.day == 1)]
    data_periods['Previous Month'] = series_to_json(pmo.drop(columns=['Timestamp']))

    # yearly
    yo = data[(data['Timestamp'].dt.year == datetime.now().year) & (data['Timestamp'].dt.day == 1) & (
            data['Timestamp'].dt.month == 1)]
    data_periods['Yearly'] = series_to_json(yo.drop(columns=['Timestamp']))

    # previous week
    pwo = data[(data['Timestamp'].dt.day_of_week == 0) & (data['Timestamp'].dt.day == 1)].iloc[-1]
    data_periods['Previous Week'] = series_to_json(pwo.drop(columns=['Timestamp']))

    # daily
    do = data.iloc[-1]
    data_periods['Daily'] = series_to_json(do.drop(columns=['Timestamp']))

    # previous day open
    pdo = data.iloc[-2]
    data_periods['Previous Day'] = series_to_json(pdo.drop(columns=['Timestamp']))

    print(f"OVHL of {symbol}: {data_periods}")

    notify_data_periods(data_periods)

    return data_periods


def notify_data_periods(data_periods):
    symbol = data_periods['symbol']
    # todo: split: complex filter
    which_users_following = PeriodicTask.objects.filter(name__contains=symbol).values('name')
    which_users_following = [i['name'].split('_')[0] for i in which_users_following]
    print(f"Following users: {which_users_following}")

    which_users_following = TelegramActive.objects.filter(username__in=which_users_following)
    for usr in which_users_following:
        print(f"Notifying {usr}")
        chat_id = usr.chat_id
        TelegramDataService.get_system_bot(True)
        TelegramDataService.bot.send_message(chat_id, data_periods)


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
