from django.contrib.auth import load_backend
from rest_framework import serializers


class CharityLoginSerializer(serializers.Serializer):
    """
    CharityLoginSerializer is a serializer class that is used to validate the charity_name and password fields
    when a charity is trying to log in.

    It contains the following fields:
    - charity_name: A CharField that represents the name of the charity.
    - password: A CharField that represents the password of the charity.

    It contains the following methods:
    - auth_charity: A method that authenticates the charity using the charity_name and password fields.
    """

    # Fields
    charity_name = serializers.CharField()
    password = serializers.CharField()

    # noinspection PyMethodMayBeStatic
    def auth_charity(self, cleaned_data):
        """
        A method to authenticate the charity using the charity_name and password fields.

        :param cleaned_data: A dictionary containing the charity_name and password fields.

        :return: Authenticated charity or ValidationError
        """

        # Making a dictionary of the credentials
        credentials = {
            'charity_name': cleaned_data['charity_name'],
            'password': cleaned_data['password']
        }

        # Using the CharityNameBackend to authenticate the charity
        backend = load_backend('CharityAPI.backends.CharityNameBackend')

        # Authenticating the charity
        charity = backend.authenticate(request=None, **credentials, backend=backend)

        # If the charity is authenticated and is active, return the charity
        if charity and charity.is_active:
            return charity
        else:
            raise serializers.ValidationError('Incorrect charity name or password.')
