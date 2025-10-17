from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission

from materials.models import Lesson, Course
from users.models import User


class LessonViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_author = User.objects.create_user(email='author@test.ru', password='pass')
        cls.user_moderator = User.objects.create_user(email='moderator@test.com', password='pass')
        cls.user_moderator.is_staff = True
        cls.user_regular = User.objects.create_user(email='regular@test.com', password='pass')

        group, created = Group.objects.get_or_create(name='Moderators')

        add_permission = Permission.objects.get(codename='add_lesson')
        delete_permission = Permission.objects.get(codename='delete_lesson')
        change_permission = Permission.objects.get(codename='change_lesson')
        view_permission = Permission.objects.get(codename='view_lesson')

        group.permissions.remove(add_permission)
        group.permissions.remove(delete_permission)
        group.permissions.add(change_permission)
        group.permissions.add(view_permission)

        cls.user_moderator.groups.add(group)
        cls.user_moderator.save()

        cls.course = Course.objects.create(name='Test', description='Test course', author=cls.user_author)
        cls.lesson = Lesson.objects.create(name='Test Lesson', description='1234', link_video='youtube.com',
                                           course=cls.course, author=cls.user_author)

        cls.url_create = reverse('materials:create_lesson')
        cls.url_update = reverse('materials:update_lesson', kwargs={'pk': cls.lesson.pk})  # если нужен pk
        cls.url_list = reverse('materials:list_lesson')
        cls.url_detail = reverse('materials:lesson_details', kwargs={'pk': cls.lesson.pk})
        cls.url_delete = reverse('materials:delete_lesson', kwargs={'pk': cls.lesson.pk})

    def test_create_lesson_authenticated(self):
        data = {
            'name': 'New lesson',
            'description': 'Description text',
            'link_video': 'https://youtube.com/newvideo',
            'course': self.course.id,
        }

        self.client.force_authenticate(user=self.user_regular)

        response = self.client.post(self.url_create, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().author, self.user_author)

    def test_delete_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user_regular)

        response = self.client.delete(self.url_delete)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_moderator_cannot_create_lesson(self):
        data = {
            'name': 'New lesson',
            'description': 'Description text',
            'link_video': 'https://youtube.com/newvideo',
            'course': self.course.id,
        }

        self.client.force_authenticate(user=self.user_moderator)

        response = self.client.post(self.url_create, data=data, format='json')

        self.assertTrue(self.user_moderator.groups.filter(name='Moderators').exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.user_moderator)

        response = self.client.delete(self.url_delete)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_create_lesson_author(self):
        data = {
            'name': 'New lesson',
            'description': 'Description text',
            'link_video': 'https://youtube.com/newvideo',
            'course': self.course.id,
        }

        self.client.force_authenticate(user=self.user_author)

        response = self.client.post(self.url_create, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().author, self.user_author)

    def test_delete_lesson_author(self):
        self.client.force_authenticate(user=self.user_author)

        response = self.client.delete(self.url_delete)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_update_lesson_author(self):
        self.client.force_authenticate(user=self.user_author)

        data = {'name': 'New lesson 1'}

        response = self.client.patch(self.url_update, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'New lesson 1')
        self.assertEqual(self.lesson.author, self.user_author)

    def test_update_lesson_regular(self):
        self.client.force_authenticate(user=self.user_regular)

        data = {'name': 'New lesson 1'}

        response = self.client.patch(self.url_update, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Test Lesson')
        self.assertEqual(self.lesson.author, self.user_author)

    def test_update_lesson_moderator(self):
        self.client.force_authenticate(user=self.user_moderator)

        data = {'name': 'New lesson 1'}

        response = self.client.patch(self.url_update, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'New lesson 1')
        self.assertEqual(self.lesson.author, self.user_author)