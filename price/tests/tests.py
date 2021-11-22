from datetime import datetime

import ccxt
import pandas as pd
from matplotlib import dates as mpl_dates
from matplotlib import pyplot as plt
from mpl_finance import candlestick_ohlc

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
exchange.set_sandbox_mode(True)
symbol = 'BTC/USDT'
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
t_frame = '5m'

# fetch data
btc_saatlik_50 = exchange.fetch_ohlcv(symbol, t_frame)
btc_saatlik_50 = pd.DataFrame(btc_saatlik_50, columns=header)
btc_saatlik_50['Timestamp'] = [datetime.utcfromtimestamp(i // 1000) for i in btc_saatlik_50.Timestamp]
# btc_saatlik_50.Timestamp = btc_saatlik_50.Timestamp.to_timestamp()
btc_saatlik_50.rename(columns={'Timestamp': 'Date'}, inplace=True)
btc_saatlik_50.drop(columns=['Volume'], inplace=True)


# support resistance: test
def is_support(df, i):
    support = df['Low'][i] < df['Low'][i - 1] < df['Low'][i - 2] and df['Low'][i] < df['Low'][i + 1] < df['Low'][
        i + 2]

    return support


def is_resistance(df, i):
    resistance = df['High'][i] > df['High'][i - 1] > df['High'][i - 2] and df['High'][i] > df['High'][i + 1] > \
                 df['High'][i + 2]

    return resistance


def collect_levels(df):
    levels = []
    for i in range(2, df.shape[0] - 2):
        if is_support(df, i):
            levels.append((i, df['Low'][i]))
        elif is_resistance(df, i):
            levels.append((i, df['High'][i]))

    return levels


def plot_all(df):
    fig, ax = plt.subplots()

    candlestick_ohlc(ax, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    #
    # date_format = mpl_dates.DateFormatter('%d %b %Y')
    # ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    for level in levels:
        plt.hlines(level[1], xmin=df['Date'][level[0]], \
                   xmax=max(df['Date']), colors='blue')
    return fig


dataframe = btc_saatlik_50
levels = collect_levels(dataframe)

fig = plot_all(dataframe)
fig.show()
