from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
import datetime as dt
import requests

# stuff used to access the openweathermap api
api_key = "***REMOVED***"
api_url = "https://api.openweathermap.org/data/2.5/weather?"

# this class holds a method to get the weather in any city through an api request to openweathermap
# in the get request it must be passed a json string with the city name in the form {'city' : 'London'}
class GetWeather(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        city = request.query_params.get('city', '')  # Fetch 'city' from query parameters

        if not city:
            return Response({'error': 'City parameter is required'}, status=400)

        input_url = api_url + "q=" + city + "&appid=" + api_key
        response = requests.get(input_url)

        # Check if the request was successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Failed to fetch weather data'}, status=response.status_code)

