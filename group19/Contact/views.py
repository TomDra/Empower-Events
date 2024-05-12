from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ContactMessage
import json

@csrf_exempt
def submit_contact_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name', '')
        email = data.get('email')
        message = data.get('message')
        if request.user.is_authenticated:
            ContactMessage.objects.create(name=name, email=email, message=message, user=request.user)
        else:
            ContactMessage.objects.create(name=name, email=email, message=message)
        return JsonResponse({"status": "success", "message": "Thank you for your message."})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
