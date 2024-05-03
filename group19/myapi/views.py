from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello,  happy world! (Django)'})

# Create your views here.
from django.http import JsonResponse
from .models import Activity, Feedback, Calendar
from django.shortcuts import get_object_or_404

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
