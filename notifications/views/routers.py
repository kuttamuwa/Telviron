from rest_framework import routers
from notifications.views.api import ExchangeAPI, WatchAssetAPI, CryptoAssetAPI, TelegramRegisterAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'exchanges', ExchangeAPI)
router.register(r'watch', WatchAssetAPI)

router.register(r'asset/crypto', CryptoAssetAPI)
router.register(r'register/telegram', TelegramRegisterAPI.as_view(), basename='register-telegram')
