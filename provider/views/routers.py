from rest_framework import routers

from provider.views.api import DovizAPI, SarrafiyeAPI, HesaplananSarrafiyeAPI, DovizHistoryAPI, SarrafiyeHistoryAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'doviz', DovizAPI)
router.register(r'sarrafiye', SarrafiyeAPI)
router.register(r'milyem', HesaplananSarrafiyeAPI, basename='milyem')

# history
router.register(r'doviz_h', DovizHistoryAPI)
router.register(r'sarrafiye_h', SarrafiyeHistoryAPI)
