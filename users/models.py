from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите электронную почту')
    phone_number = models.CharField(max_length=15, verbose_name='Phone')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    city = models.CharField(max_length=50, verbose_name='city', help_text='Введите свой город')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):
    STATUS_CHOICES = [
        ('cash', 'Наличными',),
        ('bank card', 'Банковской картой')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный урок')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=STATUS_CHOICES, default='cash', max_length=9, verbose_name='Способ оплаты')

    def __str__(self):
        target = self.course.name if self.course else (self.lesson.name if self.lesson else 'Без цели')
        return f'Поступление от пользователя {self.user.email} оплаты за {target} в размере {self.payment_amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['user', 'payment_amount', 'payment_date']