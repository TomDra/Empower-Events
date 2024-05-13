"""
The views module for the EventsAPI app
"""
import os

from rest_framework.parsers import MultiPartParser
from django.utils import timezone
from rest_framework import permissions, generics, pagination, status, renderers
from EventsAPI.serializers import CalendarSerializer, CalendarSerializerAddEvent, ActivityLeaderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsCharity
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



class PastEventsList(generics.ListAPIView):
    """
    PastEventsList class is a subclass of ListAPIView. It is used to list past events in pages.
    It contains the following methods:
    - get_queryset (get): A method to get the queryset of past events.
    """
    # Setting the serializer, permission classes, and pagination class.
    serializer_class = CalendarSerializer
    permission_classes = []#permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        """
        A method to get the queryset of past events.

        :return: A queryset of past events.
        """

        # Return past events
        return Calendar.objects.filter(time__lt=timezone.now()).select_related('activity').order_by('-time')

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

    def get_queryset(self):
        """
        A method to get the queryset of past events.

        :return: A queryset of past events.
        """

        # Return past events
        return Calendar.objects.filter(time__lt=timezone.now()).select_related('activity').order_by('-time')


class AddEvent(APIView):
    """
    EXAMPLE QUERY:
{
  "activity": {
    "title": "title test",
    "description": "event desc",
    "latitude": 2,
    "longitude": 1,
    "age_group": {
      "age_range_lower": 5,
      "age_range_higher": 10,
      "group_title": "Kids"
    },
    "compatible_disabilities": [
      "wheelchair user"
    ],
    "photo_file_path": "activity2.jpg"
  },
  "time": "2024-09-15T10:00:00Z",
  "activity_leader_id": 22
}
    """
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
            'title':activity.title,
            'description': activity.description,
            'latitude': activity.latitude,
            'longitude': activity.longitude,
            'compatible_disabilities': activity.get_compatible_disabilities(),
            'charity_name': activity.charity.charity_name,
            'age_group': {
                'lower': activity.age_group.age_range_lower,
                'higher': activity.age_group.age_range_higher,
                'title': activity.age_group.group_title,
            },
            'photo_file_path': activity.photo_file_path
            
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


class AddEventPhoto(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated, IsCharity]

    def post(self, request):
        """
        A method to add an activity photo.

        :param request: The request object.

        :return: A response containing the event photo file path or the errors if the data is invalid.
        """
        if request.FILES.get('photo'):
            photo = request.FILES['photo']

            # Assuming you have a 'media' directory in your project root
            media_path = 'media/activity_images/'
            if not os.path.exists(media_path):
                os.makedirs(media_path)

            # Generate a unique file name
            file_name = photo.name
            file_name_and_path = os.path.join(media_path, file_name)

            # Check if file already exists
            count = 1
            while os.path.exists(file_name_and_path):
                file_name = f"{os.path.splitext(file_name)[0]}_{count}{os.path.splitext(file_name)[1]}"
                file_name_and_path = os.path.join(media_path, file_name)
                count += 1

            # Save the image file
            with open(file_name_and_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)

            # Return the file name in the response
            return Response({'file_name': file_name}, status=status.HTTP_201_CREATED)

        # Return errors if the request method is not POST or no file is provided
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

