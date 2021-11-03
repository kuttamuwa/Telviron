from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=15, name='Telephone')

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']


class PhoneSMSVerify(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, name='code')

    class Meta:
        db_table = 'PhoneSMS'


