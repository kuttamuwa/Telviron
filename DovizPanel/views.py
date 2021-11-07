from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from usrapp.models.models import CustomUser


def main_page(request):
    return render(request, 'home.html')

