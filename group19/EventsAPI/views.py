# Importing necessary libraries and modules
from django.utils import timezone
from rest_framework import permissions, generics, pagination, renderers

from EventsAPI.serializers import CalendarSerializer
from django.http import JsonResponse
from myapi.models import Activity, Feedback, Calendar
from django.shortcuts import get_object_or_404
from datetime import datetime


class UpcomingEventsList(generics.ListAPIView):
    """
    UpcomingEventsList class is a subclass of ListAPIView. It is used to list upcoming events in pages.
    It contains the following methods:
    - get_queryset (get): A method to get the queryset of upcoming events.
    """

    # Setting the serializer, permission classes, and pagination class.
    serializer_class = CalendarSerializer
    permission_classes = []#permissions.IsAuthenticated]
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
    permission_classes = []#permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        """
        A method to get the queryset of upcoming events.

        :return: A queryset of upcoming events.
        """

        # Return previous events
        return Calendar.objects.filter(time__lt=timezone.now()).select_related('activity').order_by('-time')

def event_detail(request, event_id):
    event = get_object_or_404(Activity, pk=event_id)
    feedbacks = Feedback.objects.filter(calendar_event__activity=event)  # Getting feedback associated with this event
    feedback_texts = [feedback.activity_feedback_text for feedback in feedbacks if feedback.activity_feedback_text]
    calendar = get_object_or_404(Calendar, pk=event_id)  #

    time_readable = calendar.time.strftime('%Y-%m-%d | %H:%M:%S')


    data = {
        'activity_id': event.pk,
        'description': event.description,
        'latitude': event.latitude,
        'longitude': event.longitude,
        'compatible_disabilities': event.get_compatible_disabilities(),
        'charity_name': event.charity.charity_name,
        'age_group': {
            'lower': event.age_group.age_range_lower,
            'higher': event.age_group.age_range_higher,
            'title': event.age_group.group_title,
        },
        'feedback': feedback_texts,
        'timeDate': time_readable,
    }
    return JsonResponse(data)