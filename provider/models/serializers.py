from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from provider.models.models import Doviz, SarrafiyeMilyem, DovizH, SarrafiyeMilyemH
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
    # todo: deprecated
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


# HISTORY
class DovizHistorySerializer(ModelSerializer):
    instance = serializers.SlugRelatedField(slug_field='kur', read_only=True)
    yeni_alis = serializers.SerializerMethodField('get_instance_alis')
    yeni_satis = serializers.SerializerMethodField('get_instance_satis')

    class Meta:
        model = DovizH
        fields = '__all__'

    def get_instance_alis(self, obj):
        return obj.instance.alis

    def get_instance_satis(self, obj):
        return obj.instance.satis

    def get_instance_kur(self, obj):
        return obj.instance.kur


class SarrafiyeMilyemHistorySerializer(ModelSerializer):
    instance_kur = serializers.SerializerMethodField('get_instance_kur')
    yeni_alis = serializers.SerializerMethodField('get_instance_alis')
    yeni_satis = serializers.SerializerMethodField('get_instance_satis')

    class Meta:
        model = SarrafiyeMilyemH
        fields = ('instance_kur', 'yeni_alis', 'yeni_satis',
                  'old_alis', 'old_satis', 'update_date', 'source')

    def get_instance_alis(self, obj):
        return obj.instance.alis

    def get_instance_satis(self, obj):
        return obj.instance.satis

    def get_instance_kur(self, obj):
        return obj.instance.kur
