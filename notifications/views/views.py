from django.contrib import messages
# Create your views here.
from django.views.generic import FormView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import AdminRenderer
from rest_framework.views import APIView

from notifications.forms.registration.telegram import TelegramRegisterForm


class TelegramRegisterView(FormView):
    template_name = 'notifications/registration/telegram.html'
    form_class = TelegramRegisterForm
    success_message = '{TelegramNotification} updated successfully !'

    authentication_classes = [
        # IsAuthenticated
    ]

    permission_classes = [
        # IsAuthenticated
    ]

    renderer_classes = [
        AdminRenderer
    ]

    def form_valid(self, form):
        response = super(TelegramRegisterView, self).form_valid(form)
        success_messages = self.get_success_message(form.cleaned_data)

        if success_messages:
            messages.success(self.request, success_messages)

        return response

    def get_success_message(self, cleaned_data):
        return self.success_message.format(TelegramNotification=cleaned_data.get('TelegramNotification'))

    def get_success_url(self):
        return self.request.path
