from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        print("Notification is up !")
        from notifications.scripts.telegram_initial import add_telegram_system_bot
        # from notifications.services.telegram.ITelegram import TelegramDataService

        # TelegramDataService.get_system_bot(True)

        # telegram setup
        add_telegram_system_bot()
