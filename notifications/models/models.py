from django.db import models

# Create your models here.
from notifications.models.managers import BaseNotificationManager, WatchManager
from usrapp.models.models import CustomUser


# Notification models
class BaseNotification(models.Model):
    notifier = models.CharField(max_length=50, name='Notifier', verbose_name='Notifier')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, name='created_date', verbose_name='Created Date')

    manager = BaseNotificationManager

    class Meta:
        abstract = True


class TelegramNotification(BaseNotification):
    notifier = 'TELEGRAM'
    token = models.CharField(max_length=50, null=False, blank=False, unique=True)


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
    name = models.CharField(max_length=10, name='Name', verbose_name='Name',
                            help_text='Ex: Bitcoin, Etherium, Solana etc.')
    symbol = models.CharField(max_length=10, name='Symbol', verbose_name='Symbol',
                              help_text='Attention: /USD parity will be analyzed. Ex: BTC, ETH, SOL etc. ')
    exchanges = models.ForeignKey(Exchanges, on_delete=models.CASCADE)

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

    created_date = models.DateTimeField(auto_now_add=True, name='created_date', verbose_name='Created Date')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    manager = WatchManager

    def __str__(self):
        return f"Watching : {self.asset}"

    class Meta:
        abstract = False
        db_table = 'WATCH_CRYPTO'
