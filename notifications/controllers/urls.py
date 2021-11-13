from django.urls import path, include

from notifications.views.routers import router
from notifications.views.views import TelegramRegisterView

urlpatterns = [
    path('api/', include(router.urls)),

    path('register/telegram/', TelegramRegisterView.as_view()),

]
