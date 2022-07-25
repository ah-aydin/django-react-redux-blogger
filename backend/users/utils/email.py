from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .token import generate_token
from ..models import User

import threading

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
        
    def run(self):
        self.email_message.send()

def send_activation_email(request, user: User):
    current_site = get_current_site(request)
    email_subject = 'Activate your blogger account'
    message = render_to_string('users/email/activate.html', {
        'user': user,
        'domain': current_site.domain,
        'activation_url': settings.USERS['ACTIVATION_URL'],
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    
    email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    thread = EmailThread(email_message)
    thread.start()
    return thread

def send_password_reset_email(request, user: User):
    pass