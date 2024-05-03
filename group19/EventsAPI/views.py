# Importing necessary libraries and modules
from django.utils import timezone
from rest_framework import permissions, generics, pagination, renderers

from EventsAPI.serializers import CalendarSerializer
from myapi.models import Calendar


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
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        """
        A method to get the queryset of upcoming events.

        :return: A queryset of upcoming events.
        """

        # Return upcoming events
        return Calendar.objects.filter(time__gte=timezone.now()).select_related('activity').order_by('time')
    
class PreviousEventsList(generics.ListAPIView):
    """
    PreviousEventsList class is a subclass of ListAPIView. It is used to list previous events in pages.
    It contains the following methods:
    - get_queryset (get): A method to get the queryset of upcoming events.
    """

    # Setting the serializer, permission classes, and pagination class.
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        """
        A method to get the queryset of upcoming events.

        :return: A queryset of upcoming events.
        """

        # Return previous events
        return Calendar.objects.filter(time__lt=timezone.now()).select_related('activity').order_by('-time')
