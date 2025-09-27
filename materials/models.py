from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50)
    preview = models.ImageField(upload_to='preview/', verbose_name='preview')
    description = models.TextField()

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    preview = models.ImageField(upload_to='preview/', verbose_name='preview')
    description = models.TextField()
    link_video = models.URLField(max_length=200)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['name']

    def __str__(self):
        return self.name