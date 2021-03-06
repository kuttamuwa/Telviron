from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from usrapp.views.routers import router
from usrapp.views.views import main_page, LoginView, UserAPIView, CustomTokenObtainPairView, LogoutView

urlpatterns = [
    path('api/', include(router.urls)),

    # authentication
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('sms', SMSView.as_view(), name='sms'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('current_user/', UserAPIView.as_view(), name='user'),

    path('', main_page)
]
