from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from price.models.models import Exchanges, CryptoAsset, WatchCryptoAsset
from price.models.serializers import ExchangeSerializer, CryptoAssetSerializer, WatchAssetSerializer


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
