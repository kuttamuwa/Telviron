from rest_framework import serializers
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        validated_data['created_by'] = validated_data.pop('user')
        return super(MakasSerializer, self).create(validated_data)

    class Meta:
        model = Makas
        # fields = '__all__'
        exclude = ('created_by', )