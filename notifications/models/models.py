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
    name = models.CharField(name='Name', verbose_name='Name')
    url = models.URLField(name='url', verbose_name='url')

    class Meta:
        abstract = True
        db_table = 'EXCHANGES'


# Asset Models
class BaseAsset(models.Model):
    name = models.CharField(max_length=10, name='Name', verbose_name='Name')
    symbol = models.CharField(max_length=10, name='Symbol', verbose_name='Symbol')
    exchanges = models.ForeignKey(Exchanges, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CryptoAsset(BaseAsset):
    class Meta:
        abstract = False
        db_table = 'CRYPTO_ASSET'


# Watch Models
class WatchAsset(models.Model):
    asset = models.ForeignKey(BaseAsset, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True, name='created_date', verbose_name='Created Date')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    manager = WatchManager
