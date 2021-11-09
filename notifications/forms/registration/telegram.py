from django import forms

from notifications.models.models import TelegramNotification


class TelegramRegisterForm(forms.ModelForm):
    class Meta:
        model = TelegramNotification
        fields = '__all__'


