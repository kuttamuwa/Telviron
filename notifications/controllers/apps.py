from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        print("Notification is up !")
        from notifications.scripts.telegram_initial import add_telegram_system_bot
        from notifications.scheduled.telegram import tele_service

        # telegram setup
        add_telegram_system_bot()
        tele_service = tele_service
