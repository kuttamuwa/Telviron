# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import AdminRenderer
from rest_framework.views import APIView

from price.models.models import Exchanges, CryptoAsset, WatchCryptoAsset


class ExchangeView(APIView):
    queryset = Exchanges.objects.all()

    authentication_classes = [

    ]
    permission_classes = [
        IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer
    ]


class CryptoAssetView(APIView):
    queryset = CryptoAsset.objects.all()

    authentication_classes = [

    ]
    permission_classes = [
        IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer
    ]


class WatchAssetView(APIView):
    queryset = WatchCryptoAsset.objects.all()

    authentication_classes = [

    ]
    permission_classes = [
        IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer
    ]
