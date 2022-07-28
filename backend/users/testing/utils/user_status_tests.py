from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User
from users.utils.user_status import activate_user, reset_password
from users.utils.token import token_generator

class UtilsUserStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('dummy@gmail.com', 'dummy', 'password')
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = token_generator.make_token(self.user)
        self.wrong_uid = urlsafe_base64_encode(force_bytes(12312312321))
        self.wrong_token = 'some random token'

    def test_activate_user_correct_data(self):
        is_activated = activate_user(self.uid, self.token)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(is_activated, True)
        self.assertEqual(user.is_active, True)
        
    def test_activate_user_incorrect_data(self):
        is_activated = activate_user(self.wrong_uid, self.wrong_token)
        
        self.assertEqual(is_activated, False)
        self.assertEqual(self.user.is_active, False)
        
    def test_reset_password_corret_data(self):
        password_is_reset = reset_password(self.uid, self.token, 'new password')
        self.assertEqual(password_is_reset, True)
    
    def test_reset_password_wrong_data(self):
        password_is_reset = reset_password(self.wrong_uid, self.wrong_token, 'new password')
        self.assertEqual(password_is_reset, False)