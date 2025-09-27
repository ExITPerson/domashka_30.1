from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите электронную почту')
    phone_number = models.CharField(max_length=15, verbose_name='Phone')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    city = models.CharField(max_length=50, verbose_name='city', help_text='Введите свой город')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email