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

