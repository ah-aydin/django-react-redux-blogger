from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.test import TestCase
from django.template.loader import render_to_string
from django.test.client import RequestFactory
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

from users.models import User
from users.utils import email
from users.utils.token import token_generator

class UtilsEmailTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('dummy@gmail.com', 'dummy', 'password')
    
    def test_send_activation_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        request = self.factory.post(reverse('user-activate', kwargs={'uidb64': uid, 'token': token}))
        current_site = get_current_site(request)
        
        thread = email.send_activation_email(request, self.user)
      
        expected_subject = 'Activate your blogger account'
        expected_body = render_to_string('users/email/activate.html', {
            'user': self.user,
            'domain': current_site.domain,
            'activation_url': settings.USERS['ACTIVATION_URL'],
            'uid': uid,
            'token': token
        })
        thread.join()
        
        self.assertEqual(mail.outbox[-1].subject, expected_subject)
        self.assertEqual(mail.outbox[-1].body, expected_body)