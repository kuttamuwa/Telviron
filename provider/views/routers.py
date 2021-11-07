from rest_framework import routers

from provider.views.api import DovizAPI, SarrafiyeAPI, HesaplananSarrafiyeAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'doviz', DovizAPI)
router.register(r'sarrafiye', SarrafiyeAPI)
router.register(r'milyem', HesaplananSarrafiyeAPI, basename='milyem')
