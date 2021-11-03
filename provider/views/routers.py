from rest_framework import routers

from provider.views.api import DovizAPI, DovizMobilAPI, MakasAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'doviz', DovizAPI)
router.register(r'dovizmobil', DovizMobilAPI)
router.register(r'makas', MakasAPI)