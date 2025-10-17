from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from materials.models import Course
from users.models import User, Subscription


class SubscriptionAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='user@test.com', password='pass')
        cls.course = Course.objects.create(name='Course 1', description='desc', author=cls.user)

        cls.url_subscription_list = reverse('users:subscription')
        cls.url_subscription_manage = reverse('users:subscription-manage', kwargs={'course_id': cls.course.id})

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_subscriptions(self):
        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.get(self.url_subscription_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
        self.assertEqual(response.data[0]['course'], self.course.id)

    def test_post_subscription_toggle_add_and_remove(self):
        response_add = self.client.post(self.url_subscription_list, data={'course_id': self.course.id}, format='json')
        self.assertEqual(response_add.status_code, status.HTTP_200_OK)
        self.assertEqual(response_add.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response_remove = self.client.post(self.url_subscription_list, data={'course_id': self.course.id}, format='json')
        self.assertEqual(response_remove.status_code, status.HTTP_200_OK)
        self.assertEqual(response_remove.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_manage_subscription_post_create(self):
        response = self.client.post(self.url_subscription_manage)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Подписка успешно оформлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_manage_subscription_post_exists(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(self.url_subscription_manage)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Подписка уже оформлена')

    def test_manage_subscription_delete_exists(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(self.url_subscription_manage)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_manage_subscription_delete_not_exists(self):
        response = self.client.delete(self.url_subscription_manage)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Вы не подписаны на этот курс')
