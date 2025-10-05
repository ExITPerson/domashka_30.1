from django.core.management.base import BaseCommand
from users.models import User, Payments
from materials.models import Course, Lesson

class Command(BaseCommand):
    help = 'Fill database with sample data'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'phone_number': '+79991234567',
                'city': 'Москва'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()

        course = Course.objects.create(
            name='Python Basics',
            description='Основы программирования на Python'
        )

        lesson = Lesson.objects.create(
            name='Введение в Python',
            description='Первое знакомство с языком',
            link_video='https://youtube.com/watch?v=test',
            course=course
        )

        Payments.objects.create(
            user=user,
            course=course,
            payment_amount=1000.00,
            payment_method='cash'
        )

        self.stdout.write(self.style.SUCCESS('Данные успешно заполнены!'))