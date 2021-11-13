from celery import shared_task
import ccxt

"""


"""


@shared_task
def decoy(symbol, exchange='binance', direction='up'):
    exc = getattr(ccxt, exchange)
    ccxt.binance.fetch

class Guardian(object):
    """
    No asset can escape on my watch
    """
    pass
