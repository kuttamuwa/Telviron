"""
Author: Umut Ucok, 2021
"""

from rest_framework import authentication, exceptions


# class DumanOTPAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         username = request.META.get('HTTP_X_USERNAME')
