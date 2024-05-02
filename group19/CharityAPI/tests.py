# Importing necessary libraries/modules from Django and rest_framework
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Getting the User model from Django
User = get_user_model()


# A test case for the CharityAPI
class CharityAPITest(TestCase):
    
    def setUp(self):
        # Creating a test client
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='charity',
            password='password')

    # Test charity login
    def test_charity_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'charity',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test login with invalid password
    def test_invalid_charity_login_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'charity',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test login with invalid username
    def test_invalid_charity_login_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'notCharity',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test charity logout
    def test_charity_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test logout without being logged in
    def test_unauthorised_charity_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
