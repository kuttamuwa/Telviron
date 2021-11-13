from django.apps import AppConfig


class ProviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'provider'

    def ready(self):
        from provider.scheduled_tasks.ozbey import pull_data
        from usrapp.models.models import CustomUser
        from provider.controllers.signals import doviz_log_changes
        # pull_data()
