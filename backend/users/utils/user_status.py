from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode

from .token import token_generator
from ..models import User

def activate_user(uidb64, token) -> bool:
    uid = smart_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return False
    if token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    return False

def reset_password(user, password) -> bool:
    pass