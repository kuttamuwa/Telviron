from provider.views.routers import router
from provider.views.views import main_page
from django.urls import include, path

urlpatterns = [
    path('api/', include(router.urls)),

    path('', main_page)
]