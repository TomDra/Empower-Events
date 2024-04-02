# Importing necessary libraries and modules
from django.utils import timezone
from rest_framework import permissions, generics

from EventsAPI.serializers import CalendarSerializer
from myapi.models import Calendar


class EventsUpcomingList(generics.ListAPIView):
    """
    EventsUpcomingList class is a subclass of ListAPIView. It is used to list upcoming events.
    It contains the following methods:
    - get_queryset (get): A method to get the queryset of upcoming events.
    """

    # Setting the serializer class and permission classes
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        A method to get the queryset of upcoming events.

        :return: A queryset of upcoming events.
        """

        # Return the next 20 upcoming events
        return Calendar.objects.filter(time__gte=timezone.now()).select_related('activity').order_by('time')[:20]
