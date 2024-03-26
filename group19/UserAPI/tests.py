# Importing the necessary modules and classes.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Getting the User model from Django
User = get_user_model()


# Base test case for the UserAPI
class UserAPITest(TestCase):
    def setUp(self):
        """
        Set up the test case with a test client and a test user.
        """
        self.client = APIClient()
        self.user = self.create_user(
            username='TestUser',
            password='password',
            email='testUser@email.com'
        )

    # noinspection PyMethodMayBeStatic
    def create_user(self, username, password, email):
        """
        Helper method to create a user.
        """
        return User.objects.create_user(username=username, password=password, email=email)

    def post_request(self, url_name, data):
        """
        Helper method to make a post request.
        """
        return self.client.post(reverse(url_name), data)


class UserLoginTest(UserAPITest):
    # Test user login
    def test_user_login(self):
        """
        Test that a user can log in with valid credentials.
        """
        response = self.post_request('login', {
            'username': 'TestUser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test login with wrong password
    def test_invalid_user_login_password(self):
        """
        Test that a user cannot log in with an incorrect password.
        """
        response = self.post_request('login', {
            'username': 'TestUser',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test login with wrong username
    def test_invalid_user_login_username(self):
        """
        Test that a user cannot log in with an incorrect username.
        """
        response = self.post_request('login', {
            'username': 'wrongUser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_user_login_credentials(self):
        """
        Test that a user cannot log in with an incorrect username and password.
        """
        response = self.post_request('login', {
            'username': 'wrongUser',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_user_login_credentials(self):
        """
        Test that a user cannot log in with empty username and password.
        """
        response = self.post_request('login', {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_malformed_user_login_credentials(self):
        """
        Test that a user cannot log in with malformed json.
        """
        response = self.post_request('login', {
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTest(UserAPITest):
    # Test user logout
    def test_user_logout(self):
        """
        Test that a logged-in user can log out.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test logout without being logged in
    def test_unauthorised_user_logout(self):
        """
        Test that a user cannot log out if they are not logged in.
        """
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserRegistrationTest(UserAPITest):
    # Test user registration
    def test_user_registration(self):
        """
        Test that a user can register with valid data.
        """
        user_data = {'username': 'NewUser', 'password': 'Password123', 'email': 'newuser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test registration with an existing username
    def test_user_registration_existing_username(self):
        """
        Test that a user cannot register with an existing username.
        """
        user_data = {'username': 'TestUser', 'password': 'Password123', 'email': 'unique@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration with an existing email
    def test_user_registration_existing_email(self):
        """
        Test that a user cannot register with an existing email.
        """
        user_data = {'username': 'unique', 'password': 'Password123', 'email': 'testUser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration with an invalid username
    def test_registration_invalid_username(self):
        """
        Test that a user cannot register with an invalid username.
        """
        user_data = {'username': 'abc', 'password': 'Password123', 'email': 'unique@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration with an invalid email.
    def test_registration_invalid_email(self):
        """
        Test that a user cannot register with an invalid email.
        """
        user_data = {'username': 'NewUser', 'password': 'Password123', 'email': 'invalidEmail'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration with password less than 8 characters
    def test_registration_password_less_than_8_characters(self):
        """
        Test that a user cannot register with a password less than 8 characters.
        """
        user_data = {'username': 'NewUser', 'password': 'Pass12', 'email': 'newuser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration without uppercase letters in password
    def test_registration_password_without_uppercase(self):
        """
        Test that a user cannot register without at least one uppercase letter in the password.
        """
        user_data = {'username': 'NewUser', 'password': 'password123', 'email': 'newuser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration without lowercase letters in password
    def test_registration_password_without_lowercase(self):
        """
        Test that a user cannot register without at least one lowercase letter in the password.
        """
        user_data = {'username': 'NewUser', 'password': 'PASSWORD123', 'email': 'newuser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration without digits in password
    def test_registration_password_without_digits(self):
        """
        Test that a user cannot register without at least one digit in the password.
        """
        user_data = {'username': 'NewUser', 'password': 'Password', 'email': 'newuser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration while a user is logged in.
    def test_registration_while_logged_in(self):
        """
        Test that a user cannot register while they are logged in.
        """
        self.client.force_login(self.user)
        user_data = {'username': 'NewUser', 'password': 'Password123', 'email': 'newuser@email.com'}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration with empty fields
    def test_registration_empty_fields(self):
        """
        Test that a user cannot register with empty fields.
        """
        user_data = {'username': '', 'password': '', 'email': ''}
        response = self.post_request('register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test registration with malformed json
    def test_registration_malformed_json(self):
        """
        Test that a user cannot register with malformed json.
        """
        response = self.post_request('register', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
