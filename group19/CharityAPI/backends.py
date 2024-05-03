from django.contrib.auth.backends import ModelBackend
from myapi.models import Charity


class CharityNameBackend(ModelBackend):
    """
    CharityNameBackend class is a subclass of ModelBackend. It is used to authenticate a charity by their charity name.
    It contains the following methods:
    - authenticate: A method to authenticate a charity by their charity name.
    - get_user: A method to get a charity by their user id.
    """

    def authenticate(self, request, charity_name=None, password=None, **kwargs):
        """
        A method to authenticate a charity by their charity name.

        :param request: The request object.
        :param charity_name: The charity name.
        :param password: The charity password.
        :param kwargs: Additional keyword arguments.

        :return: The charity object if the charity is authenticated, else None.
        """

        # Check if the charity name exists in the database
        try:
            charity = Charity.objects.get(charity_name=charity_name)
        except Charity.DoesNotExist:
            return

        # Check if the charity password is correct
        if charity.check_password(password):
            return charity

    def get_user(self, user_id):
        """
        A method to get a charity by their user id.

        :param user_id: The user id.

        :return: The charity object if the charity exists, else None.
        """

        try:
            return Charity.objects.get(pk=user_id)
        except Charity.DoesNotExist:
            return
