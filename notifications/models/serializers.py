from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from notifications.models.models import Exchanges, CryptoAsset, WatchCryptoAsset


class ExchangeSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Exchanges


class CryptoAssetSerializer(ModelSerializer):
    # exchanges = serializers.CharField(source='exchanges.name')

    class Meta:
        fields = '__all__'
        model = CryptoAsset


class WatchAssetSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WatchCryptoAsset
