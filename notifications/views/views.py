from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import AdminRenderer
from rest_framework.views import APIView

from notifications.models.models import Exchanges, CryptoAsset, WatchAsset


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
    queryset = WatchAsset.objects.all()

    authentication_classes = [

    ]
    permission_classes = [
        IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer
    ]
