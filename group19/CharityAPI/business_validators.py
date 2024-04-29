# TODO: Implement classes for charity creation.
import re

from django.core.exceptions import ValidationError
from .validators import CharityNameValidator as BaseNameValidator
from .validators import PasswordValidator as BasePasswordValidator


from myapi.models import Charity


class CharityNameValidator(BaseNameValidator):
    """
    CharityNameValidator class is a subclass of BaseNameValidator. It is used to validate the charity_name field using
    business rules/logic.

    It contains the following methods:
    - validate: A method to validate the charity_name field using business rules/logic.
    """

    @classmethod
    def validate(cls, charity_name):
        """
        A method to validate the charity_name field using business rules/logic.

        :param charity_name: The charity_name to be validated.

        :return: True if the charity_name is valid.
        """
        super().validate(charity_name)

        # Check if the charity_name is unique.
        if Charity.objects.filter(charity_name=charity_name).exists():
            raise ValidationError('Charity name already exists.')
        if len(charity_name) > 50:
            raise ValidationError('Username must be at least 5 characters long.')
        return True


class PasswordValidator(BasePasswordValidator):
    """
    PasswordValidator class is a subclass of BasePasswordValidator. It is used to validate the password field using
    business rules/logic.

    It contains the following methods:
    - validate: A method to validate the password field using business rules/logic.
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
