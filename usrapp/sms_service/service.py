"""

"""
import requests

from usrapp.models.models import CustomUser

from config import settings

SMS_API = settings.SMS_SERVICE


def send_sms(content: str, body: str, subject: str,
             users: [CustomUser], **kwargs):
    """
    TODO: .
    Send SMS to SMS Service
    :param content:
    :param body:
    :param subject:
    :param users:
    :param kwargs:
    :return:
    """
    for usr in users:
        to = usr.telephone

        content = None

        requests.post(
            SMS_API.auth_url,
            headers={'Authorization': SMS_API.token},
            data=content
        )