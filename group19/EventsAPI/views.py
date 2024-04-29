"""
The views module for the EventsAPI app
"""
from django.utils import timezone
from rest_framework import permissions, generics, pagination, status

from EventsAPI.serializers import CalendarSerializer, EventSerializer
from myapi.models import Calendar
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsActivityLeader


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
    It contains the following methods:
    - post: A method to add an event.
    """

    # Setting the permission classes.
    permission_classes = [permissions.IsAuthenticated, IsActivityLeader]

    def post(self, request):
        """
        A method to add an event.

        :param request: The request object.
        :return: Response object with status 201 if the event is added, else 400/500.
        """

        # Passing the request data to the EventSerializer.
        serializer = EventSerializer(data=request.data, context={'request': request})

        # If the serializer is valid, save the event and return a response with status 201.
        if serializer.is_valid():
            event = serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        # If the serializer is not valid, return a response with status 400.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

