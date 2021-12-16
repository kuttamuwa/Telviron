from django.apps import AppConfig


class PriceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'price'

    def ready(self):
        print("Price is up !")
        # from price.models.models import DiaryNew, DiaryAction, DiaryChart
