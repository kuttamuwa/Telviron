import random

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from usrapp.models.models import PhoneSMSVerify
from usrapp.models.serializers import CustomUserSerializer


def main_page(request):
    return render(
        request,
        'usrapp/usrapp.html'
    )


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        phone_number = user.telephone

        user_serialize = CustomUserSerializer(user, many=False)
        request.session['user'] = user_serialize.data

        # get token
        tkn = RefreshToken.for_user(user)

        # sms sending
        sifre = self.send_sms(phone_number)

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


class SMSView(APIView):
    def post(self, request, format=None):
        usr = request.user
        sifre = request.POST['sifre']
        print(f"Sifre : {sifre}")
        phone_sms = PhoneSMSVerify.objects.get(user=request.user, code=sifre)

        return Response({
            'access': phone_sms.access_token,
            'refresh': phone_sms.refresh_token
        })
