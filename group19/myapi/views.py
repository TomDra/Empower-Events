from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello,  happy world! (Django)'})

# Create your views here.
from django.http import JsonResponse
from .models import Activity
from django.shortcuts import get_object_or_404

def event_detail(request, event_id):
    event = get_object_or_404(Activity, pk=event_id)
    # Assuming `charity` is the related name for the ForeignKey in Activity model to Charity
    data = {
        'activity_id': event.pk,
        'description': event.description,
        'compatible_disabilities': event.get_compatible_disabilities(),  # Assuming this is a method to get JSON-loaded disabilities
        'charity_name': event.charity.charity_name  # Accessing charity_name from the related Charity model
    }
    return JsonResponse(data)
