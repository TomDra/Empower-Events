# Importing the necessary modules and classes.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()

class WeatherAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def testGetWeather(self):
        response = self.client.get(reverse('getWeather'), {"city" : "London"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)