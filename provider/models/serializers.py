from rest_framework.serializers import ModelSerializer

from provider.models.models import Doviz


class DovizSerializer(ModelSerializer):
    class Meta:
        model = Doviz
        fields = '__all__'

