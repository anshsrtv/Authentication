from django.db import models
from django.contrib.auth.models import AbstractUser
from django_cryptography.fields import encrypt

class User(AbstractUser):
    name = encrypt(models.CharField(max_length=300))
    email = models.EmailField(max_length=64, unique=True)
    authy_id = models.IntegerField(unique=True, null=True, blank=True)
    contact = models.CharField(max_length=10)
    phone_verified = models.BooleanField(default=False)

