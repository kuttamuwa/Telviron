from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from provider.models.models import Doviz  # , Makas
import logging

from provider.scheduled_tasks.ozbey import ozbey_tarih_format

logger = logging.getLogger(__name__)


class DovizSerializer(ModelSerializer):
    class Meta:
        model = Doviz
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(DovizSerializer, self).to_representation(instance)

        return ret


class HistorySerializer(Serializer):
    kur = serializers.CharField()

    eski_alis = serializers.FloatField()
    yeni_alis = serializers.FloatField()

    eski_tarih = serializers.DateTimeField(format=ozbey_tarih_format)
    yeni_tarih = serializers.DateTimeField(format=ozbey_tarih_format)

# class MakasSerializer(ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     created_by = serializers.ReadOnlyField(source='created_by.username')
#     kur = serializers.SlugRelatedField(many=False, read_only=False, slug_field='kur',
#                                        queryset=Doviz.objects.all())
#
#     def create(self, validated_data):
#         validated_data['created_by'] = validated_data.pop('user')
#         logger.info(f'Yeni makas değeri : {validated_data}')
#
#         return super(MakasSerializer, self).create(validated_data)
#
#     class Meta:
#         model = Makas
#         fields = '__all__'
