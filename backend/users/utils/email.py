from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .token import token_generator
from ..models import User

import threading

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
        
    def run(self):
        self.email_message.send()

def send_activation_email(request, user: User):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    
    activation_url = settings.USER['ACTIVATION_URL'].replace(':uid', uid).replace(':token', token)
    
    current_site = get_current_site(request)
    email_subject = 'Activate your blogger account'
    message = render_to_string('users/email/activate.html', {
        'user': user,
        'domain': current_site.domain,
        'activation_url': activation_url
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

def send_password_reset_email(request, email: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise User.DoesNotExist()
    
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    
    current_site = get_current_site(request)
    email_subject = 'Reset your password'
    password_reset_url = settings.USERS['PASSWORD_RESET_URL'].replace(':uid', uid).replace(':token', token)
    
    message = render_to_string('users/email/password_reset.html', {
        'user': user,
        'domain': current_site.domain,
        'password_reset_url': password_reset_url
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