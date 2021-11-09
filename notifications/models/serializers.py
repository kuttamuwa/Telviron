from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from notifications.models.models import Exchanges, CryptoAsset, WatchAsset


class ExchangeSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Exchanges


class CryptoAssetSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CryptoAsset


class WatchAssetSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WatchAsset
