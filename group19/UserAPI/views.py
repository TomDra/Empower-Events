# Importing necessary libraries and modules from Django, rest_framework, validators, and serializers
from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserLoginSerializer
from .validators import *


class UserLogin(APIView):
    """
    UserLogin class is a subclass of APIView. It is used to authenticate a user and log them in.
    It contains the following methods:
    - post: A method to authenticate a user and log them in.
    """

    # Allow any user to login
    permission_classes = [permissions.AllowAny]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """
        A method to authenticate a user and log them in.
        TODO: Remove serializer.data from the response in production. Test only.

        :param request: The request object.
        :return: Response object with status 200 if the user is authenticated, else 400.
        """

        data = request.data
        # Validate the username and password fields
        try:
            validate_username(data)
            validate_password(data)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data=data)
        # If the serializer is valid, authenticate the user and log them in
        if serializer.is_valid():
            user = serializer.auth_user(serializer.validated_data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    """
    UserLogout class is a subclass of APIView. It is used to log a user out.
    It contains the following methods:
    - post: A method to log a user out.
    """

    # Allow only authenticated users to logout
    permission_classes = [permissions.IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
