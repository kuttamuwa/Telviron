from rest_framework.serializers import ModelSerializer

from provider.models.models import Doviz, Makas


class DovizSerializer(ModelSerializer):
    class Meta:
        model = Doviz
        fields = '__all__'


class MakasSerializer(ModelSerializer):
    class Meta:
        model = Makas
        fields = '__all__'
