from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import CustomUser
from django.contrib.auth.models import Group


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',)


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
