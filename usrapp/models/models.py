from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=15, name='Telephone')

    objects = CustomUserManager()



