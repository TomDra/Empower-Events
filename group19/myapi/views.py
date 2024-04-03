from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello,  happy world! (Django)'})

# Create your views here.
from django.http import JsonResponse
from .models import Event
from django.shortcuts import get_object_or_404

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # Serialize the event data. Adjust this according to your model fields.
    data = {
        'event_id': event.pk,
        'activity_name': event.activity_name,  # Example field
        'description': event.description,  # Example field
        'time': event.time,  # Example field
        # Add any other fields you need to return
    }
    return JsonResponse(data)
