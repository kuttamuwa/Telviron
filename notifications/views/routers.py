from rest_framework import routers

from notifications.views.api import TelegramRegisterAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'register/telegram', TelegramRegisterAPI)
