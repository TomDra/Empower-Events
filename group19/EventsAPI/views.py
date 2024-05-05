"""
The views module for the EventsAPI app
"""
from django.utils import timezone
from rest_framework import permissions, generics, pagination, status

from EventsAPI.serializers import CalendarSerializer, CalendarSerializerAddEvent, ActivityLeaderSerializer
from myapi.models import Calendar, ActivityLeader, Charity
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsCharity


class UpcomingEventsList(generics.ListAPIView):
    """
    UpcomingEventsList class is a subclass of ListAPIView. It is used to list upcoming events in pages.
    It contains the following methods:
    - get_queryset (get): A method to get the queryset of upcoming events.
    """

    # Setting the serializer, permission classes, and pagination class.
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        """
        A method to get the queryset of upcoming events.

        :return: A queryset of upcoming events.
        """

        # Return upcoming events
        return Calendar.objects.filter(time__gte=timezone.now()).select_related('activity').order_by('time')


class PastEventsList(generics.ListAPIView):
    """
    PastEventsList class is a subclass of ListAPIView. It is used to list past events in pages.
    It contains the following methods:
    - get_queryset (get): A method to get the queryset of past events.
    """

    # Setting the serializer, permission classes, and pagination class.
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        """
        A method to get the queryset of past events.

        :return: A queryset of past events.
        """

        # Return past events
        return Calendar.objects.filter(time__lt=timezone.now()).select_related('activity').order_by('-time')


class AddEvent(APIView):
    """
    AddEvent class is a subclass of APIView. It is used to add an event.
    TODO: remove serializer.data from post method

    It contains the following methods:
    - get (get): A method to get the list of all activity leaders and their user id's for the subsequent post request.
    - post (post): A method to add an event.
    """
    permission_classes = [permissions.IsAuthenticated, IsCharity]

    def get(self, request):
        """
        A method to get the list of all activity leaders and their user id's for the subsequent post request.

        :param request: The request object.

        :return: A response containing the list of all activity leaders and their user id's.
        """
        charity = Charity.objects.get(charity_name=request.user.charity_name)
        activity_leaders = ActivityLeader.objects.filter(charity=charity)
        serializer = ActivityLeaderSerializer(activity_leaders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        A method to add an event.

        :param request: The request object.

        :return: A response containing the added event or the errors if the data is invalid.
        """

        # Create a new event
        serializer = CalendarSerializerAddEvent(data=request.data, context={'request': request})

        # Check if the data is valid
        if serializer.is_valid():
            # Save the event
            serializer.save()

            # Return the added event
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

