from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        from notifications.models.models import TelegramNotification
        from usrapp.models.models import CustomUser
        from notifications.scripts.ccxt_initial import add_exchanges_auto
        from notifications.scripts.telegram_initial import add_telegram_system_bot
        from notifications.services.telegram import ITelegram

        # telegram setup
        add_telegram_system_bot()

        # ccxt initial data
        add_exchanges_auto()
