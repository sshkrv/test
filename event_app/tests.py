from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestUser(APITestCase):
    def test_user_registration(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        url = reverse('register')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username='testuser').username, 'testuser')

    def test_user_registration_with_already_taken_username(self):
        User.objects.create_user(username='testuser', password='testpass')

        data = {'username': 'testuser', 'password': 'testpass2'}
        url = reverse('register')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass')

        data = {'username': 'testuser', 'password': 'testpass'}
        url = reverse('login')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_user_login_with_wrong_credentials(self):
        User.objects.create_user(username='testuser', password='testpass')

        data = {'username': 'testuser', 'password': 'wrongpass'}
        url = reverse('login')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

