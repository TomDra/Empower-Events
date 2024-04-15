# Importing necessary libraries/modules from Django and rest_framework
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

# Getting the User model from Django
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer class is a subclass of ModelSerializer that serializes the User model.
    It contains 'username' and 'email' fields from the expected User model.
    """

    class Meta:
        model = User
        fields = ['username', 'email']


class UserLoginSerializer(serializers.Serializer):
    """
    UserLoginSerializer class is a subclass of Serializer that validates the user login data.
    It contains 'username' and 'password' fields.
    """

    username = serializers.CharField()
    password = serializers.CharField()

    # noinspection PyMethodMayBeStatic
    def auth_user(self, cleaned_data):
        """
        A method to authenticate the user using the username and password fields.

        :param cleaned_data: A dictionary containing the username and password fields.
        :return: Authenticated user or ValidationError
        """

        username_field = User.USERNAME_FIELD

        credentials = {
            username_field: cleaned_data['username'],
            'password': cleaned_data['password']
        }

        user = authenticate(**credentials)

        if user:
            return user
        else:
            raise serializers.ValidationError('Incorrect username or password.')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    UserRegisterSerializer class is a subclass of ModelSerializer that serializes the User model.
    It contains all fields from the expected User model.
    """

    class Meta:
        model = User
        fields = '__all__'

    def create(self, cleaned_data):
        """
        A method to create a new user using the username, email, and password fields.

        :param cleaned_data: A dictionary containing the username, email, and password fields.
        :return: The newly created user.
        """

        username_field = User.USERNAME_FIELD

        credentials = {
            username_field: cleaned_data['username'],
            'email': cleaned_data['email'],
            'password': cleaned_data['password']
        }

        # Create a new user
        user = User.objects.create_user(**credentials)
        user.save()
        return user
