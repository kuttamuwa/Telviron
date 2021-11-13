import ccxt
import pandas as pd
import requests

from price.models.models import Exchanges


def add_exchanges_auto():
    # pull from github
    url = "https://github.com/ccxt/ccxt/wiki/Exchange-Markets#supported-exchanges"
    res = pd.read_html(url)[0]

    for _, row in res[['id', 'name']].iterrows():
        ex, status = Exchanges.objects.get_or_create(
            name=row['name'],
            ccxt_id=row['id']
        )
        if status:
            print(f"Exchange eklendi : {ex}")
