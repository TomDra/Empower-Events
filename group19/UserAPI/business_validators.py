# Importing necessary libraries/modules from Django, validators, and re (regular expressions).
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re

from .validators import UsernameValidator as BaseUsernameValidator
from .validators import PasswordValidator as BaseEmailValidator
from .validators import PasswordValidator as BasePasswordValidator

# Getting the User model from Django
User = get_user_model()


class UsernameBusinessValidator(BaseUsernameValidator):
    """
    A class to validate the username field using business rules/logic.
    """
    @classmethod
    def validate(cls, username):
        """
        A method to validate the username field using business rules/logic.

        :param username: The username to be validated.
        :return: True if the username is valid.
        """
        super().validate(username)

        # Check if the username is at least 5 characters long.
        if len(username) < 5:
            raise ValidationError('Username must be at least 5 characters long.')
        # Check if the username is unique.
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return True


class EmailBusinessValidator(BaseEmailValidator):
    """
    A class to validate the email field using business rules/logic.
    """
    @classmethod
    def validate(cls, email):
        """
        A method to validate the email field using business rules/logic.

        :param email: The email to be validated.
        :return: True if the email is valid.
        """
        super().validate(email)

        # Check if the email is valid.
        EmailValidator()(email)
        # Check if the email is unique.
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return True


class PasswordBusinessValidator(BasePasswordValidator):
    """
    A class to validate the password field using business rules/logic.
    """
    @classmethod
    def validate(cls, password):
        """
        A method to validate the password field using business rules/logic.

        :param password: The password to be validated.
        :return: True if the password is valid.
        """
        super().validate(password)

        # Check if the password is at least 8 characters long.
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        # Check if the password contains at least one uppercase letter.
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        # Check if the password contains at least one lowercase letter.
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        # Check if the password contains at least one digit.
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one digit.')
        return True
