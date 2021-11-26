from datetime import date, timedelta, datetime

from celery import shared_task

from price.models.models import DATE_ACTION_ENUMS, EMA_ENUMS
from config import settings
import ccxt
import pandas as pd

# only exchange for now
exchange = ccxt.binance()


def ovhl_hourly_since_yesterday(symbol):
    """
    Default latest 24 hour whole data per hour timeframe
    :param symbol: BTC/USDT
    :return:
    """
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%dT%H:%M:%S')
    yesterday = exchange.parse8601(yesterday)

    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    t_frame = "1h"
    asset_data = exchange.fetch_ohlcv(symbol, timeframe=t_frame, since=yesterday)
    asset_data = pd.DataFrame(asset_data, columns=header)
    asset_data['Timestamp'] = [datetime.utcfromtimestamp(i // 1000) for i in asset_data.Timestamp]

    return asset_data


def get_sma(symbol, length=20, time_frame='1D'):
    assert time_frame in [i[0] for i in EMA_ENUMS]

    asset_data = exchange.fetch
