from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User, Follow

TEST_USER = {
    'email': 'email@gmail.com',
    'username': 'ciuciuc',
    'password': '1_sffVVdasdSO*FAx'
}

def get_client_authenticated():
    """
    Create an active account, return it's tokens and authenticate
    """
    client = APIClient()

    # Create account
    account = User.objects.create_user(**TEST_USER)
    account.is_active = True
    account.save()

    # Log in to get user tokens
    response = client.post(reverse('auth-tokens'), TEST_USER, format='json')
    access = response.data['access']

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    return client, account
