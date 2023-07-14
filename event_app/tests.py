from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Event


class TestEvent(APITestCase):
    """
        This class tests the Event functionality.
        It includes tests for event creation, retrieving event list and details,
        registering and unregistering to an event, and checking event capacity.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        start_date = timezone.now() + timedelta(days=1)
        self.event = Event.objects.create(
            creator=self.user,
            title='Test Event',
            description='Test Description',
            date=start_date,
            type='Test Type',
            status='Test Status',
            capacity=10
        )

    def test_create_event(self):
        """
            Test that an event is created successfully.
        """
        self.client.login(username='testuser', password='testpass')

        start_date = timezone.now() + timedelta(hours=2)

        data = {
            'creator': self.user.id,
            'title': 'Test Event 2',
            'description': 'Test Description 2',
            'date': start_date,
            'type': 'Test Type 2',
            'status': 'Test Status 2',
            'capacity': 20
        }
        url = reverse('event-list')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.get(title='Test Event 2').title, 'Test Event 2')

    def test_list_own_events(self):
        """
            Test that a user can retrieve a list of their own events.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('event-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_event_detail(self):
        """
            Test that a user can retrieve the details of a specific event.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_register_event(self):
        """
            Test that a user can register for an event.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('event-register')
        response = self.client.post(url, {'event_id': self.event.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get(username='testuser') in Event.objects.get(id=self.event.id).attendees.all())

    def test_unregister_event(self):
        """
            Test that a user can unregister from an event.
        """
        self.client.login(username='testuser', password='testpass')
        self.event.attendees.add(self.user)
        url = reverse('event-register') + '?event_id=' + str(self.event.id)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.get(username='testuser') in Event.objects.get(id=self.event.id).attendees.all())

    def test_event_capacity(self):
        """
            Test that a user cannot register for an event that has reached its capacity.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('event-register')
        self.event.capacity = 1
        self.event.save()
        self.event.attendees.add(User.objects.create_user(username='testuser2', password='testpass2'))

        response = self.client.post(url, {'event_id': self.event.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUser(APITestCase):
    """
        This class tests the User functionality.
        It includes tests for user registration and login.
    """
    def test_user_registration(self):
        """
            Test that a user is registered successfully.
        """
        data = {'username': 'testuser', 'password': 'testpass'}
        url = reverse('register')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username='testuser').username, 'testuser')

    def test_user_registration_with_already_taken_username(self):
        """
            Test that a user cannot register with a username that is already taken.
        """
        User.objects.create_user(username='testuser', password='testpass')

        data = {'username': 'testuser', 'password': 'testpass2'}
        url = reverse('register')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """
            Test that a user can log in successfully.
        """
        User.objects.create_user(username='testuser', password='testpass')

        data = {'username': 'testuser', 'password': 'testpass'}
        url = reverse('login')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_user_login_with_wrong_credentials(self):
        """
            Test that a user cannot log in with wrong credentials.
        """
        User.objects.create_user(username='testuser', password='testpass')

        data = {'username': 'testuser', 'password': 'wrongpass'}
        url = reverse('login')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


