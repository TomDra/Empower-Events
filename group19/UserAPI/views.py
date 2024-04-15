# Importing necessary libraries and modules from Django, rest_framework, validators, and serializers
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

<<<<<<< HEAD
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .validators import *
||||||| cebae78
from .serializers import UserLoginSerializer
from .validators import *
=======
from .business_validators import UsernameBusinessValidator, PasswordBusinessValidator, EmailBusinessValidator
from .serializers import UserLoginSerializer, UserRegisterSerializer
from .validators import UsernameValidator, PasswordValidator
>>>>>>> trunk


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
        :return: Response object with status 200 if the user is authenticated, else 400/500.
        """

        data = request.data
        # Validate the username and password fields
        try:
            # Check if the username and password fields are present in the request data
            if data.get('username') is None or data.get('password') is None:
                raise ValidationError('Username and password are required.')

            # Validate the username and password fields
            UsernameValidator.validate(data['username'])
            PasswordValidator.validate(data['password'])
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response('An error has occurred.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
<<<<<<< HEAD
    

||||||| cebae78
=======


class UserRegister(APIView):
    """
    UserRegister class is a subclass of APIView. It is used to register a new user.
    It contains the following methods:
    - post: A method to register a new user.
    """

    # Allow any user to register
    permission_classes = [permissions.AllowAny]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """
        A method to register a new user.
        TODO: Remove serializer.data from the response in production. Test only.

        :param request: The request object.
        :return: Response object with status 201 if the user is registered, else 400/500.
        """

        # Checking if the user is already authenticated.
        if request.user.is_authenticated:
            return Response('User is already authenticated.', status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        # Validate the username, email, and password fields.
        try:
            UsernameBusinessValidator.validate(data['username'])
            EmailBusinessValidator.validate(data['email'])
            PasswordBusinessValidator.validate(data['password'])
        except KeyError:
            return Response('Username, email, and password are required.', status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response('An error has occurred.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = UserRegisterSerializer(data=data)
        # If the serializer is valid, create a new user.
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> trunk
