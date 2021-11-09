from rest_framework import routers
from notifications.views.api import ExchangeAPI, WatchAssetAPI, CryptoAssetAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'exchanges/', ExchangeAPI)
router.register(r'watch/', WatchAssetAPI)
router.register(r'asset/crypto/', CryptoAssetAPI)
