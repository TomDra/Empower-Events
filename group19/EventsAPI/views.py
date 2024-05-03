# Importing necessary libraries and modules
from django.utils import timezone
from rest_framework import permissions, generics, pagination, renderers

from EventsAPI.serializers import CalendarSerializer
from django.http import JsonResponse
from myapi.models import Activity, Feedback, Calendar, ActivityLeader, Charity
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

def activity_detail(request, activity_id):
    event = get_object_or_404(Activity, pk=activity_id)
    #feedbacks = Feedback.objects.filter(calendar_event__activity=event)  # Getting feedback associated with this event
    #feedback_texts = [feedback.activity_feedback_text for feedback in feedbacks if feedback.activity_feedback_text]
    #calendar = Calendar.objects.filter(event_id=event_id)  #

    #time_readable = calendar.time.strftime('%Y-%m-%d | %H:%M:%S')


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
        #'feedback': feedback_texts,
        #'timeDate': time_readable,
    }
    return JsonResponse(data)

def calander_details(self, event_id):
    calendar_event = get_object_or_404(Calendar, pk=event_id)
    activity = get_object_or_404(Activity, pk=calendar_event.activity_id)
    activity_leader = get_object_or_404(ActivityLeader, pk=calendar_event.activity_leader_id)
    charity = get_object_or_404(Charity, pk=activity_leader.charity_id)

    time_readable = calendar_event.time.strftime('%Y-%m-%d | %H:%M:%S')

    data = {
        'activity':{
            'activity_id': activity.pk,
            'description': activity.description,
            'latitude': activity.latitude,
            'longitude': activity.longitude,
            'compatible_disabilities': activity.get_compatible_disabilities(),
            'charity_name': activity.charity.charity_name,
            'age_group': {
                'lower': activity.age_group.age_range_lower,
                'higher': activity.age_group.age_range_higher,
                'title': activity.age_group.group_title,
            }
        },
        'timeDate': time_readable,
        'event_leader':{
            "name": activity_leader.name,
            "email": activity_leader.email,
            "birthday": activity_leader.birth_date
        },
        'charity': {
            'name': charity.charity_name,
            'email': charity.email,
        }

    }
    return JsonResponse(data)