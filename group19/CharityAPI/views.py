# Importing necessary libraries and modules from Django, rest_framework, validators, and serializers
from django.contrib.auth import login, logout
from rest_framework.exceptions import APIException
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Uses serializer and validator from UserAPI for now
# TODO: Write new specialised serializer and validator for charity logins once the model becomes more set in stone
from UserAPI.serializers import UserLoginSerializer#, CharityLoginSerializer
from UserAPI.validators import *



class CharityLogin(APIView):
    """
    CharityLogin class is a subclass of APIView. It is used to authenticate a charity and log them in.
    It contains the following methods:
    - post: A method to authenticate a charity and log them in.
    """


    # Allow any user to login
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        A method to authenticate a charity and log them in.
        TODO: Remove serializer.data from a successful response.

        :param request: The request object.
        :return: Response object with status 200 if the charity is authenticated, else 400/500.
        """

        data = request.data

        try:
            if data.get('charity_name') is None or data.get('password') is None:
                raise ValidationError('Charity name and password are required.')

            # Validate the charity name and password fields
            CharityNameValidator.validate(data['charity_name'])
            PasswordValidator.validate(data['password'])

        except ValidationError as e:
            # Return the error message and a response code of 400
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            # Return the error message and a response code of 500
            return Response('An error has occurred.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Return the error message and a response code of 500
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create a serializer instance
        # serializer = CharityLoginSerializer(data=data)

        # # Check if the serializer is valid
        # if serializer.is_valid():
        #     # Authenticate the charity
        #     charity = serializer.auth_charity(serializer.validated_data)

        #     # Log the charity in
        #     login(request, charity)

        #     # Return a response code of 200
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     # Return the errors and a response code of 400
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharityLogout(APIView):
    """
    CharityLogout class is a subclass of APIView. It is used to log a charity out.
    It contains the following methods:
    - post: A method to log a charity out.
    """

    # Allow only authenticated users to logout
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        A method to log out a charity.

        :param request: The request object.
        :return: Response object with status 200.
        """
        

        # Log the charity out
        logout(request)

        # Return a response code of 200
        return Response(status=status.HTTP_200_OK)
