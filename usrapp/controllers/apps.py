from django.apps import AppConfig


class UsrappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usrapp'

    def ready(self):
        from usrapp.models.models import CustomUser, CustomUserManager
        from usrapp.controllers.admin import CustomUser
