from django.contrib.auth.models import Group
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .fields import DumanPhoneNumberField
from .models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',)


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
