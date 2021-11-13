import logging
import random

import requests
from django.conf import settings as django_settings
from rest_framework.exceptions import APIException

from config import settings
from ..models.models import PhoneSMSVerify, CustomUser

logger = logging.getLogger(__name__)


class DumanSMSService:
    url = "http://www.ozteksms.com/panel/smsgonder1Npost.php"
    headers = {'Content-Type': "application/xml"}
    _from = "905323028251"

    @classmethod
    def generate_send_sms(cls, phone_number):
        sifre = random.randint(1000, 10000)
        message = f"<sms><kno>1007268</kno><kulad>905323028251</kulad><sifre>568SYR</sifre><tur>Normal</tur><gonderen>" \
                  f"AVIMAYDNLTM</gonderen><mesaj>GUNES DOVIZ PANEL GIRIS SIFRENIZ : {sifre}</mesaj><numaralar>" \
                  f"{phone_number}</numaralar>" \
                  f"<zaman>2020-01-14 10:56:00</zaman><zamanasimi>2020-01-14 11:56:00</zamanasimi></sms>"

        # TODO: BURAYI AC
        # response = requests.post(cls.url, data={'data': message})
        # print(f"SMS Gonderme servisi response : {response}")

        print(f"Saved sms code object ! : {sifre}")

        return sifre

