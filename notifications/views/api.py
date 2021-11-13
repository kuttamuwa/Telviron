from django.views.generic import FormView
from rest_framework.renderers import AdminRenderer
from rest_framework.viewsets import ModelViewSet

from notifications.forms.registration.telegram import TelegramRegisterForm
from notifications.models.models import TelegramNotification
from notifications.models.serializers import TelegramNotificationSerializer


class TelegramRegisterAPI(ModelViewSet):
    queryset = TelegramNotification.objects.all()
    serializer_class = TelegramNotificationSerializer

    authentication_classes = [
        # IsAuthenticated
    ]
    permission_classes = [
        # IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer

    ]


class TelegramRegisterView(FormView):
    queryset = TelegramNotification.objects.all()

    template_name = 'provider/set_doviz.html'
    form_class = TelegramRegisterForm
    success_message = '{doviz} başarıyla güncellendi'
