import random

from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from usrapp.models.models import PhoneSMSVerify, CustomUser
from usrapp.models.serializers import CustomUserSerializer


def main_page(request):
    return render(
        request,
        'usrapp/usrapp.html'
    )


class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        phone_number = user.telephone

        # get token
        tkn = RefreshToken.for_user(user)
        request.session['access_token'] = tkn.access_token
        request.session['refresh_token'] = tkn

        # sms sending
        sifre = self.send_sms(phone_number)
        print(f"şifre : {sifre}")
        messages.success(request, 'Şifre gönderildi')

        # save token and sms code
        phone_sms = PhoneSMSVerify.objects.update_or_create(user=user, code=sifre,
                                                            access=tkn.access_token, refresh=tkn)[0]

        # redirect sms page
        return render(request, 'usrapp/SMS Page.html')

    @staticmethod
    def send_sms(phone_number):
        sifre = random.randint(10000, 99999)

        message = f"<sms><kno>1007268</kno><kulad>905323028251</kulad><sifre>568SYR</sifre><tur>Normal</tur><gonderen>" \
                  f"AVIMAYDNLTM</gonderen><mesaj>GUNES DOVIZ PANEL GIRIS SIFRENIZ : {sifre}</mesaj><numaralar>" \
                  f"{phone_number}</numaralar>" \
                  f"<zaman>2020-01-14 10:56:00</zaman><zamanasimi>2020-01-14 11:56:00</zamanasimi></sms>"

        return sifre


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()

        return Response(
            status=status.HTTP_200_OK
        )


class SMSView(APIView):
    def post(self, request, format=None):
        sifre = request.POST['sifre']

        usr = request.session['user']
        refresh_token = request.session['refresh_token']
        access_token = request.session['access_token']

        # verify now
        try:
            phone_sms = PhoneSMSVerify.objects.get(user=usr, refresh_token=refresh_token, access_token=access_token,
                                                   code=sifre)


        except PhoneSMSVerify.DoesNotExist:
            messages.error(self.request, 'Kayıt bulunamadı !')

        if format == 'json':
            # return token informations (no matter if was exposed due to not verified in front of the castle yet)

            return Response({
                'access': phone_sms.access_token,
                'refresh': phone_sms.refresh_token
            })

        else:
            return render(request, '/tabela')
