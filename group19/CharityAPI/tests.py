# Importing necessary libraries/modules from Django and rest_framework
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapi.models import Charity


class CharityAPITest(TestCase):
    """
    Base test case for the Charity API.
    """
    def setUp(self):
        """
        Set up the test case with a test client and a test charity.
        """
        self.client = APIClient()
        self.charity = self.create_charity(
            charity_name='TestCharity',
            password='password',
            email='testCharity@email.com'
        )

    # noinspection PyMethodMayBeStatic
    def create_charity(self, charity_name, password, email):
        """
        Helper method to create a charity.
        """
        return Charity.objects.create_charity(charity_name=charity_name, password=password, email=email)

    def post_request(self, url_name, data):
        """
        Helper method to make a post request.
        """
        return self.client.post(reverse(url_name), data)


class CharityLoginTest(CharityAPITest):
    # Test charity login
    def test_charity_login(self):
        """
        Test that a charity can log in with valid credentials.
        """
        response = self.post_request('loginCharity', {
            'charity_name': 'TestCharity',
        }
                                     )
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


class CharityLogoutTest(CharityAPITest):
    """
    Test case for the charity logout endpoint.
    """

    def test_charity_logout(self):
        """
        Test that a charity can log out.
        """

        # First, log in the charity
        self.client.login(charity_name='TestCharity', password='password')

        # Then, log out the charity
        response = self.client.post(reverse('logoutCharity'))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the charity is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)

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
