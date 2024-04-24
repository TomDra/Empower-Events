from django.core.mail import send_mail

#example
def send_welcome_email(to_email):
    send_mail(
        'Welcome to Our Service',
        'Here is the message.',
        'from@example.com',
        [to_email],
        fail_silently=False,
    )
    
#example usage
#user_email = 'user@example.com'
#send_welcome_email(user_email)