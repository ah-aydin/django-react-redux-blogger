from pkg_resources import require
from rest_framework import serializers
from .models import User, Follow

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
    followers_url = serializers.HyperlinkedIdentityField(view_name='user-followers-list')
    follows_url = serializers.HyperlinkedIdentityField(view_name='user-follows-list')
    class Meta:
        model = User
        fields = (
            'url', 'id', 'email', 'username', 'date_joined', 'last_login', 'blog_count', 'followers_url', 'follows_url'
        )

class FollowingSerializer(serializers.HyperlinkedModelSerializer):
    follows_url = serializers.HyperlinkedRelatedField(view_name='user-detail', source='follows', read_only=True)
    follows_username = serializers.CharField(source='follows.username')
    class Meta:
        model = Follow
        fields = (
            'follows_url', 'follows_username',
        )

class UserFollowerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='follower.pk')
    username = serializers.CharField(source='follower.username')
    email = serializers.CharField(source='follower.email')
    follower_url = serializers.HyperlinkedRelatedField(view_name='user-detail', source='follower', read_only=True)
    class Meta:
        model = Follow
        fields = (
            'follower_url', 'id', 'username', 'email'
        )