from django.core.exceptions import ValidationError


class CharityNameValidator:
    """
    CharityNameValidator class to validate the charity name field.

    It contains the following methods:
    - validate: A method to validate the charity name field.
    """

    @classmethod
    def validate(cls, charity_name):
        """
        A method to validate the username field.

        :param charity_name: The charity name to be validated.
        :return: True if the charity name is valid.
        """

        charity_name = charity_name.strip()

        if not charity_name:
            raise ValidationError('Username field cannot be empty.')
        return True


class PasswordValidator:
    """
    PasswordValidator class to validate the password field.

    It contains the following methods:
    - validate: A method to validate the password field.
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
            raise ValidationError('Password field cannot be empty.')
        return True


