from django.db import models


class BaseNotificationManager(models.Manager):
    pass


class BaseAssetManager(models.Manager):
    pass


class WatchManager(models.Manager):
    pass
