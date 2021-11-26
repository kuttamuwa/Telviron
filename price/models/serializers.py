from rest_framework.serializers import ModelSerializer

from price.models.models import DiaryAction, DiaryNew


class DiaryActionSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = DiaryAction


class DiaryNewSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = DiaryNew