from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=50)
    preview = models.ImageField(upload_to='preview/', verbose_name='preview', null=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='course'
    )

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    preview = models.ImageField(upload_to='preview/', verbose_name='preview', null=True, blank=True)
    description = models.TextField()
    link_video = models.URLField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=None, blank=None, related_name='lessons')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='lesson'
    )

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['name']

    def __str__(self):
        return self.name