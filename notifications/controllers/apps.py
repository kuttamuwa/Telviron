from django.apps import AppConfig

from notifications.models.models import TelegramNotification
from usrapp.models.models import CustomUser


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        admin_user = CustomUser.objects.get(username='admin')
        TelegramNotification.objects.get_or_create(token='2108915600:AAEO2ZCoQGqE86gC1g_Ixd6GlVVcPH9PEBs',
                                                   user=admin_user)