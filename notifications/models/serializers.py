from rest_framework.serializers import ModelSerializer

from notifications.models.models import TelegramNotification


class TelegramNotificationSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TelegramNotification
