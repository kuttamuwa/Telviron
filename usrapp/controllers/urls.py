from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from usrapp.views.routers import router
from usrapp.views.views import main_page, LoginView, SMSView, UserAPIView

urlpatterns = [
    path('api/', include(router.urls)),

    # authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('sms', SMSView.as_view(), name='sms'),
    path('login', LoginView.as_view(), name='login'),
    path('current_user/', UserAPIView.as_view(), name='user'),

    path('', main_page)
]
