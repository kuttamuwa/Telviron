from rest_framework import routers

from usrapp.views.api import DumanVerificationViewSet
from phone_verify.api import VerificationViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'phone', DumanVerificationViewSet, basename='phone')
