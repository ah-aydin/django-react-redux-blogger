from urllib import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from users.models import User

class UserListTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-list')
    
    def test_get_users(self):
        user = User.objects.create_user('dummy@gmail.com', 'dummy', 'password')
        response = self.client.get(self.url)
        response_user = response.data['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response_user['username'], user.username)
        self.assertEqual(response_user['email'], user.email)
    
    def test_create_account(self):
        response = self.client.post(self.url, {
            'username': 'dummy', 
            'email': 'dummy@gmail.com', 
            'password': 'password', 
            're_password': 'password'}, format='json')
        users = User.objects.all()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'dummy')
        self.assertEqual(response.data['email'], 'dummy@gmail.com')
        self.assertEqual(len(users), 1)
    
    def test_reject_create_account_if_passwords_do_not_match(self):
        response = self.client.post(self.url, {
            'username': 'dummy', 
            'email': 'dummy@gmail.com', 
            'password': 'password', 
            're_password': 're_passowrd'}, format='json')
        users = User.objects.all()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(users), 0)

class UserDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('dummy@gmail.com', 'dummy', 'password')
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
    
    def test_get_user(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)