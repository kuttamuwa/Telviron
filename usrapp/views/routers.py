from rest_framework import routers

from usrapp.views.api import UsersAPI, GroupAPI

router = routers.DefaultRouter(trailing_slash=True)

# router.register(r'users', UsersAPI)
router.register(r'groups', GroupAPI)