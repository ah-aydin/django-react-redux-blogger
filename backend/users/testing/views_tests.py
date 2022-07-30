from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, Follow

from .helpers import get_client_authenticated

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
    
    def test_create_user(self):
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
    
    def test_reject_create_user_if_passwords_do_not_match(self):
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
        

class CreateDestoryFollowTests(APITestCase):
    def setUp(self):
        self.user2 = User.objects.create_superuser('dummy2@gmail.com', 'dummy2', 'dummy2')
        self.client, self.user1 = get_client_authenticated()
        
        self.url = reverse('user-create-destory-follow', kwargs={'pk': self.user1.pk})
    
    def test_not_allowd_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_destroy_follow(self):
        self.client.login(email=self.user2.email, password='dummy2')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Follow.objects.all()), 1)
        
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Follow.objects.all()), 0)

class FollowsTests(APITestCase):
    def setUp(self):
        self.client_authenticated, self.user1 = get_client_authenticated()
        self.user2 = User.objects.create_superuser('dummy2@gmail.com', 'dummy2', 'dummy2')

        # Create 2 follow object
        self.follow1 = Follow.objects.create(follower=self.user1, follows=self.user2)
        self.follow2 = Follow.objects.create(follower=self.user1, follows=self.user1)

    def test_get_followers(self):
        """
        Ensure retrieval of users followers
        """
        # Test for user1
        response = self.client.get(reverse('user-followers-list', kwargs={'pk': 1}))
        data = response.data
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)
        
        # Test for user2
        response = self.client.get(reverse('user-followers-list', kwargs={'pk': 2}))
        data = response.data
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)
        
    def test_get_follows(self):
        """
        Ensure retireval of users follows
        """
        # Test for user1
        response = self.client.get(reverse('user-follows-list', kwargs={'pk': 1}))
        data = response.data
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

        # Test for user2
        response = self.client.get(reverse('user-follows-list', kwargs={'pk': 2}))
        data = response.data
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['results']), 0)