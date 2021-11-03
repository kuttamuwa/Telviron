from django import forms

from ..models.models import CustomUser


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'password', 'telephone', 'username', 'is_active']
