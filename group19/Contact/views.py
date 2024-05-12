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
        subject = data.get('subject', '')
        message = data.get('message')

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        return JsonResponse({"status": "success", "message": "Thank you for your message."})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
