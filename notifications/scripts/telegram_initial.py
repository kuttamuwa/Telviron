from django.db import IntegrityError

from notifications.models.models import TelegramNotification
from usrapp.models.models import CustomUser


def add_telegram_system_bot():
    admin_user = CustomUser.objects.get(username='admin')
    try:
        TelegramNotification.objects.update_or_create(token='2108915600:AAEO2ZCoQGqE86gC1g_Ixd6GlVVcPH9PEBs',
                                                      user=admin_user, is_admin=True)
    except IntegrityError:
        pass
