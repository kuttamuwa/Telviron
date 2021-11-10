from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        from notifications.scripts.telegram_initial import add_telegram_system_bot

        # telegram setup
        # add_telegram_system_bot()
