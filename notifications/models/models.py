from django.db import models

# Create your models here.
from django_celery_beat.models import IntervalSchedule, PERIOD_CHOICES

from notifications.models.managers import BaseNotificationManager
from usrapp.models.models import CustomUser


# Notification models
class BaseNotification(models.Model):
    notifier = models.CharField(max_length=50, name='Notifier', verbose_name='Notifier')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, name='updated_date', verbose_name='Created Date')

    manager = BaseNotificationManager

    class Meta:
        abstract = True


class TelegramNotification(BaseNotification):
    notifier = 'TELEGRAM'
    token = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        abstract = False


class TelegramActive(models.Model):
    username = models.CharField(max_length=50, verbose_name='User name')
    chat_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'TelegramActive'


class RSSStore(models.Model):
    rss_name = models.CharField(max_length=100, verbose_name='RSS Name')
    rss_link = models.URLField(verbose_name='RSS Link')

    def __str__(self):
        return f"{self.rss_name} ||  {self.rss_link}"


class MessageStore(models.Model):
    message = models.CharField(max_length=200, verbose_name='Mesaj')
    tarih = models.DateTimeField(null=False, verbose_name='Tarih')

    def __str__(self):
        return f"Message : {self.message} \n" \
               f"Tarih : {self.tarih} \n" \
