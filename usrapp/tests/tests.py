from django.test import TestCase
from django.urls import reverse

from ..models.models import CustomUser
from rest_framework.test import APIRequestFactory, APIClient


# Create your tests here.
class UserCapTests(TestCase):
    factory = APIRequestFactory()

    def test_create_user(self):
        data = {
            'first_name': 'Test Name',
            'last_name': 'Test Surname',
            'email': 'test@gmail.com',
            'password': 'testpwd123',
            'telephone': '+905063791026',
            'is_staff': 'true',
            'is_active': 'true',
            'is_superuser': 'true',
            'groups': [1, ],

        }
        client = APIClient()
        client.post('/usrman/api/users', data, format='json')
        # req = self.factory.post('/usrman/api/users', data, format='json')
        # self.assertEqual(req.status_code, 200)
