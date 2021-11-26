from django.apps import AppConfig


global_telegram_service = None


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        print("Notification is up !")
        from notifications.scripts.telegram_initial import add_telegram_system_bot
        from notifications.services.telegram.ITelegram import TelegramDataService

        # telegram setup
        add_telegram_system_bot()

        global_telegram_service = TelegramDataService()