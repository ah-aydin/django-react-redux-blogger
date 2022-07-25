from pkg_resources import require
from rest_framework import serializers
from .models import User

class UserCreateResponseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('email', 'username')

class UserCreateSerializer(UserCreateResponseSerializer):
    re_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 're_password')
        
    def checkPassowrds(self):
        return self.data['password'] == self.data['re_password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'url', 'id', 'email', 'username', 'date_joined', 'last_login', 'blog_count'
        )