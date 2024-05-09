"""
Permissions for the FeedbackAPI.
"""
from rest_framework import permissions
from myapi.models import Charity, ActivityLeader


class IsCharityOrActivityLeader(permissions.BasePermission):
    """
    IsCharityOrActivityLeader class is a subclass of BasePermission. It checks if the user is a charity
    or an activity leader.

    It contains the following methods:
    - has_permission: A method that checks if the user is a charity or an activity leader.
    """

    def has_permission(self, request, view):
        """
        A method that checks if the user is a charity or an activity leader.

        :param request: The request object.
        :param view: The view object.
        :return: True if the user is a charity or an activity leader, False otherwise.
        """

        # Check if the user is a charity
        if isinstance(request.user, Charity):
            return True

        return False
