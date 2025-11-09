import os

from celery import shared_task
from django.core.mail import send_mail

from materials.models import Course
from users.models import Subscription
from dotenv import load_dotenv


load_dotenv(override=True)


@shared_task
def update_notification(instance_id):
    course = Course.objects.get(id=instance_id)

    subscribers = Subscription.objects.filter(course=course).values_list('user__email', flat=True)

    subject = f'Обновление курса "{course.name}"!'
    message = (f'В курсе "{course.name}" был обновлен материал, скорее переходи по ссылке, что бы ознакомиться:'
               f'http://127.0.0.1:8000/{course.id}/')

    for email in subscribers:
        send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), [email])