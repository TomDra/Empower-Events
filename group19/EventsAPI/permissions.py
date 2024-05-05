"""
Permissions module for the EventsAPI app.
"""
from rest_framework import permissions
from myapi.models import Charity


class IsCharity(permissions.BasePermission):
    """
    IsCharity class is a subclass of BasePermission. It checks if the user is a charity.

    It contains the following methods:
    - has_permission: A method that checks if the user is a charity.
    """

    def has_permission(self, request, view):
        """
        A method that checks if the user is a charity.

        :param request: The request object.
        :param view: The view object.

        :return: True if the user is a charity, False otherwise.
        """

        # Check if the user is a charity
        if isinstance(request.user, Charity):
            return True
        return False
