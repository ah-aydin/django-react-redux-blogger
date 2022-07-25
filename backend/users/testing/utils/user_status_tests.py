from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User
from users.utils.user_status import activate_user
from users.utils.token import generate_token

class UtilsUserStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('dummy@gmail.com', 'dummy', 'password')
    
    def test_activate_user_correct_data(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = generate_token.make_token(self.user)
        
        is_activated = activate_user(uid, token)
        
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(is_activated, True)
        self.assertEqual(user.is_active, True)
        
    def test_activate_user_incorrect_data(self):
        uid = urlsafe_base64_encode(force_bytes(12312312321))
        token = 'some random token'
        is_activated = activate_user(uid, token)
        
        self.assertEqual(is_activated, False)
        self.assertEqual(self.user.is_active, False)