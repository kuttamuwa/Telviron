from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from provider.models.models import Doviz, SarrafiyeMilyem  # , Makas
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


class SarrafiyeMilyemSerializer(ModelSerializer):
    class Meta:
        model = SarrafiyeMilyem
        fields = '__all__'


class SarrafiyeMilyemCalculatedSerializer(Serializer):
    kur = serializers.CharField()
    alis = serializers.FloatField()
    satis = serializers.FloatField()
