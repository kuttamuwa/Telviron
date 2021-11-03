from rest_framework.serializers import ModelSerializer

from provider.models.models import Doviz, Makas


class DovizSerializer(ModelSerializer):
    class Meta:
        model = Doviz
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(DovizSerializer, self).to_representation(instance)

        return ret


class MakasSerializer(ModelSerializer):
    class Meta:
        model = Makas
        fields = '__all__'
