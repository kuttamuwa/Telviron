import random

import requests
from phone_verify.backends import get_sms_backend
from phone_verify.backends.base import BaseBackend
from phone_verify.services import PhoneVerificationService
from rest_framework.exceptions import APIException
from config import settings
from django.conf import settings as django_settings

from ..models.models import PhoneSMSVerify, CustomUser

import logging

logger = logging.getLogger(__name__)


class DumanService(BaseBackend):
    url = "http://www.ozteksms.com/panel/smsgonder1Npost.php"
    headers = {'Content-Type': "application/xml"}
    _from = "905323028251"

    def __init__(self, **options):
        super().__init__(**options)

    def send_sms(self, phone_number, message=None):
        try:
            usr = CustomUser.objects.get(telephone=phone_number)
        except CustomUser.DoesNotExist:
            raise APIException(f'Lütfen {phone_number} telefon numaralı kullanıcının '
                               f'mevcut olduğuna emin olunuz !')

        sifre = random.randint(1000, 10000)
        message = f"<sms><kno>1007268</kno><kulad>905323028251</kulad><sifre>568SYR</sifre><tur>Normal</tur><gonderen>" \
                  f"AVIMAYDNLTM</gonderen><mesaj>GUNES DOVIZ PANEL GIRIS SIFRENIZ : {sifre}</mesaj><numaralar>" \
                  f"{phone_number}</numaralar>" \
                  f"<zaman>2020-01-14 10:56:00</zaman><zamanasimi>2020-01-14 11:56:00</zamanasimi></sms>"

        response = requests.post(self.url, data={'data': message})
        print(f"SMS Gonderme servisi response : {response}")

        user_sms = PhoneSMSVerify(user=usr, code=sifre)
        user_sms.save()

        print("Saved sms code object !")

    def send_bulk_sms(self, numbers, message=None):
        for number in numbers:
            self.send_sms(number, message)

    def validate_security_code(self, security_code, phone_number, session_token):
        """
        A utility method to verify if the `security_code` entered is valid for
        a given `phone_number` along with the `session_token` used.

        :param security_code: Security code entered for verification
        :param phone_number: Phone number to be verified
        :param session_token: Session token to identify the device

        :return stored_verification: Contains the verification object
        corresponding to the phone_number if found, else None.
        :return status: Status for the stored_verification object.
        Can be one of the following:
            - `BaseBackend.SECURITY_CODE_VALID`
            - `BaseBackend.SECURITY_CODE_INVALID`
            - `BaseBackend.SECURITY_CODE_EXPIRED`
            - `BaseBackend.SECURITY_CODE_VERIFIED`
            - `BaseBackend.SESSION_TOKEN_INVALID`
        """
        usr = CustomUser.objects.get(telephone=phone_number)

        stored_verification = PhoneSMSVerify.objects.get(
            code=security_code, user=usr
        )

        # check security_code exists
        if stored_verification is None:
            return stored_verification, self.SECURITY_CODE_INVALID

        # check session code exists
        if not stored_verification.session_token == session_token:
            return stored_verification, self.SESSION_TOKEN_INVALID

        # check security_code is not expired
        if self.check_security_code_expiry(stored_verification):
            return stored_verification, self.SECURITY_CODE_EXPIRED

        # check security_code is not verified
        if stored_verification.is_verified and django_settings.PHONE_VERIFICATION.get(
                "VERIFY_SECURITY_CODE_ONLY_ONCE"
        ):
            return stored_verification, self.SECURITY_CODE_VERIFIED

        # mark security_code as verified
        stored_verification.is_verified = True
        stored_verification.save()

        return stored_verification, self.SECURITY_CODE_VALID


class DumanPhoneVerificationService(PhoneVerificationService):
    sms_service_settings = settings.SMS_SERVICE
    verification_message = sms_service_settings.DEFAULT_MESSAGE
    backend = DumanService()

    def __init__(self, phone_number):
        self._check_required_settings()

    def _check_required_settings(self):
        pass

    def _generate_message(self, security_code):
        return self.verification_message.format(
            security_code=security_code,
        )

    def send_verification(self, number, security_code):
        message = self._generate_message(security_code)
        self.backend.send_sms(number, message)


def send_security_code_and_generate_session_token(phone_number):
    sms_backend = get_sms_backend(phone_number)
    security_code, session_token = sms_backend.create_security_code_and_session_token(
        phone_number
    )
    service = DumanPhoneVerificationService(phone_number=phone_number)
    try:
        service.send_verification(phone_number, security_code)
    except service.backend.exception_class as exc:
        logger.error(
            f"{phone_number} numarasına SMS gönderilirken bir hata oluştu: \n "
            f"{exc}"
        )
    return session_token
