# Importing necessary libraries/modules from Django and rest_framework
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Getting the User model from Django
User = get_user_model()


# A test case for the UserAPI
class UserAPITest(TestCase):
    def setUp(self):
        # Creating a test client
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='TestUser',
            password='password')

    # Test user login
    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'TestUser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test login with invalid password
    def test_invalid_user_login_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'TestUser',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test login with invalid username
    def test_invalid_user_login_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'wrongUser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test user logout
    def test_user_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test logout without being logged in
    def test_unauthorised_user_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
