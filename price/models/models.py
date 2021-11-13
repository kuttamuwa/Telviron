from django.db import models


# Create your models here.
from price.models.managers import WatchManager


class Exchanges(models.Model):
    name = models.CharField(max_length=20, name='name', verbose_name='Name', null=False)
    url = models.URLField(name='url', verbose_name='url', null=True, blank=True)
    ccxt_id = models.CharField(name='ccxt_id', verbose_name='CCXT exchange id',
                               help_text='https://ccxt.readthedocs.io/en/latest/manual.html#exchanges \n'
                                         'id column',
                               max_length=20, unique=True, null=False)

    def __str__(self):
        return f"{self.name} Exchange"

    class Meta:
        db_table = 'EXCHANGES'


# Asset Models
class BaseAsset(models.Model):
    name = models.CharField(max_length=10, name='name', verbose_name='Name',
                            help_text='Ex: Bitcoin, Etherium, Solana etc.')
    symbol = models.CharField(max_length=10, name='symbol', verbose_name='Symbol',
                              help_text='Attention: /USD parity will be analyzed. Ex: BTC, ETH, SOL etc. ')
    exchanges = models.ForeignKey(Exchanges, on_delete=models.CASCADE, name='exchanges')

    def __str__(self):
        return f"Asset : {self.name}"

    class Meta:
        abstract = True


class CryptoAsset(BaseAsset):
    def __str__(self):
        return "Crypto " + super(CryptoAsset, self).__str__()

    class Meta:
        abstract = False
        db_table = 'CRYPTO_ASSET'


# Watch Models
class WatchCryptoAsset(models.Model):
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True, name='updated_date', verbose_name='Created Date')
    creator = models.CharField(name='creator', max_length=50)

    manager = WatchManager

    def __str__(self):
        return f"Watching : {self.asset}"

    class Meta:
        abstract = False
        db_table = 'WATCH_CRYPTO'
