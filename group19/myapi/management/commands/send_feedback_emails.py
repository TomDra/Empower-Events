# your_app/management/commands/send_feedback_emails.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta
from myapi.models import Calendar

class Command(BaseCommand):
    help = 'Send feedback request emails for events that occurred a day ago'

    def handle(self, *args, **kwargs):
        yesterday = datetime.now() - timedelta(days=1)
        events = Calendar.objects.filter(time__date=yesterday.date())

        for event in events:
            subject = f"Feedback Request for {event.activity.title}"
            html_message = render_to_string('feedback_email.html', {'event': event})
            plain_message = strip_tags(html_message)
            from_email = 'from@yourdomain.com'
            to_emails = [interest.user.email for interest in event.eventinterest_set.all()]

            send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)
            self.stdout.write(self.style.SUCCESS(f'Successfully sent feedback emails for event {event.activity.title}'))

#write
#crontab -e
#then write 
#0 0 * * * /path/to/your/venv/bin/python /path/to/your/project/manage.py send_feedback_emails

#basically path to python fuile in machine and then path to manage.py