from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from usrapp.views.api import current_user
from usrapp.views.routers import router
from usrapp.views.views import main_page

urlpatterns = [
    path('api/', include(router.urls)),

    # authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('current_user/', current_user),

    path('', main_page)
]
