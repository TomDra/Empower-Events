# Importing necessary libraries/modules from Django
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Getting the User model from Django
User = get_user_model()


def validate_username(data):
    """
    A function to validate the username field.

    :param data: A dictionary containing the username field.
    :return: True if the username is not empty.
    """
    username = data['username'].strip()

    if not username:
        raise ValidationError('Username field cannot be empty.')
    return True


def validate_password(data):
    """
    A function to validate the password field.

    :param data: A dictionary containing the password field.
    :return: True if the password is not empty.
    """
    password = data['password'].strip()

    if not password:
        raise ValidationError('Password field cannot be empty.')
    return True
