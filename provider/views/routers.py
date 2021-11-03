from rest_framework import routers

from provider.views.api import DovizAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'doviz', DovizAPI)
