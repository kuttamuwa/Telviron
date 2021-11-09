from django.urls import path, include

from notifications.views.routers import router

urlpatterns = [
    path('api/', include(router.urls)),
]
