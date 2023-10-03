from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=50, **NULLABLE, verbose_name='Номер телефона')
    country = models.CharField(max_length=50, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')
    is_verified_email = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, **NULLABLE, verbose_name='Код верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
