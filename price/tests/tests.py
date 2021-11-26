from datetime import datetime

import ccxt
import pandas as pd
from matplotlib import pyplot as plt

from config import settings

# plot settings
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

# from variable id
exchange_id = 'binance'
keys = getattr(settings, exchange_id)
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': keys.API_KEY,
    'secret': keys.SECRET_KEY,
})

# virtual
# exchange.set_sandbox_mode(True)
symbol = 'BTC/USDT'
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
t_frame = '5m'

# fetch data
btc_saatlik_50 = exchange.fetch_ohlcv(symbol, t_frame)
btc_saatlik_50 = pd.DataFrame(btc_saatlik_50, columns=header)
btc_saatlik_50['Timestamp'] = [datetime.utcfromtimestamp(i // 1000) for i in btc_saatlik_50.Timestamp]
# btc_saatlik_50.Timestamp = btc_saatlik_50.Timestamp.to_timestamp()
btc_saatlik_50.rename(columns={'Timestamp': 'Date'}, inplace=True)

