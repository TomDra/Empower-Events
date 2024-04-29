"""
Permissions module for the EventsAPI app.
"""
from rest_framework import permissions
from myapi.models import ActivityLeader


class IsActivityLeader(permissions.BasePermission):
    """
    IsActivityLeader class is a subclass of BasePermission. It checks if the user is an activity leader.

    It contains the following methods:
    - has_permission: A method that checks if the user is an activity leader.
    """

    def has_permission(self, request, view):
        """
        A method that checks if the user is an activity leader.

        :param request: The request object.
        :param view: The view object.

        :return: True if the user is an activity leader, False otherwise.
        """

        # Check if the user is an activity leader
        if ActivityLeader.objects.filter(user=request.user).exists():
            return True
        return False
