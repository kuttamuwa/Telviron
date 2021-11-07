from django.urls import include, path

from usrapp.views.api import current_user
from usrapp.views.routers import router
from usrapp.views.views import main_page

urlpatterns = [
    path('api/', include(router.urls)),

    path('current_user/', current_user),

    path('', main_page)
]
