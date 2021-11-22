import ccxt

from config import settings


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
