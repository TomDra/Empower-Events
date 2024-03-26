# Importing necessary libraries/modules from Django
from django.core.exceptions import ValidationError


class UsernameValidator:
    """
    A class to validate the username field.
    """
    @classmethod
    def validate(cls, username):
        """
        A method to validate the username field.

        :param username: The username to be validated.
        :return: True if the username is valid.
        """

        username = username.strip()

        if not username:
            raise ValidationError('Username cannot be empty.')
        return True


class EmailValidator:
    """
    A class to validate the email field.
    """
    @classmethod
    def validate(cls, email):
        """
        A method to validate the email field.

        :param email: The email to be validated.
        :return: True if the email is valid.
        """

        email = email.strip()

        if not email:
            raise ValidationError('Email cannot be empty.')
        return True


class PasswordValidator:
    """
    A class to validate the password field.
    """
    @classmethod
    def validate(cls, password):
        """
        A method to validate the password field.

        :param password: The password to be validated.
        :return: True if the password is valid.
        """

        password = password.strip()

        if not password:
            raise ValidationError('Password cannot be empty.')
        return True
