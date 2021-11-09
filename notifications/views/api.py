from django.views.generic import FormView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import AdminRenderer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from notifications.forms.registration.telegram import TelegramRegisterForm
from notifications.models.models import Exchanges, CryptoAsset, WatchCryptoAsset, TelegramNotification
from notifications.models.serializers import ExchangeSerializer, CryptoAssetSerializer, WatchAssetSerializer, \
    TelegramNotificationSerializer


class ExchangeAPI(ModelViewSet):
    queryset = Exchanges.objects.all()
    serializer_class = ExchangeSerializer

    permission_classes = [
        # IsAuthenticated
    ]

    filter_backends = [
        filters.SearchFilter
    ]

    search_fields = ['name']
    ordering_fields = ['name']


class CryptoAssetAPI(ModelViewSet):
    queryset = CryptoAsset.objects.all()
    serializer_class = CryptoAssetSerializer

    permission_classes = [
        # IsAuthenticated
    ]

    filter_backends = [
        filters.SearchFilter
    ]

    search_fields = ['name', 'symbol', 'exchanges.name']
    ordering_fields = ['name']


class WatchAssetAPI(ModelViewSet):
    queryset = WatchCryptoAsset.objects.all()
    serializer_class = WatchAssetSerializer

    permission_classes = [
        # IsAuthenticated
    ]

    filter_backends = [
        filters.SearchFilter
    ]

    search_fields = ['name']
    ordering_fields = ['name']


class TelegramRegisterAPI(ModelViewSet):
    queryset = TelegramNotification.objects.all()
    serializer_class = TelegramNotificationSerializer

    authentication_classes = [
        # IsAuthenticated
    ]
    permission_classes = [
        # IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer

    ]


class TelegramRegisterView(FormView):
    queryset = TelegramNotification.objects.all()

    template_name = 'provider/set_doviz.html'
    form_class = TelegramRegisterForm
    success_message = '{doviz} başarıyla güncellendi'
