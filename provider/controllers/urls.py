from django.urls import include, path

from provider.views.routers import router
from provider.views.views import main_page, DovizFormView, TabelaView

urlpatterns = [
    path('api/', include(router.urls)),

    path('', main_page),

    # alt sayfalar
    path('admin/', DovizFormView.as_view()),
    path('tabela/', TabelaView.as_view()),
]
