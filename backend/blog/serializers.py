from asyncore import read
from pickletools import read_long1
from pkg_resources import require
from rest_framework import serializers, fields

from .models import Blog, Comment

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    comments_url = serializers.HyperlinkedIdentityField(view_name='blog-comment-list')
    author_url = serializers.HyperlinkedRelatedField(view_name='user-detail', source='author', read_only=True)
    author_pk = serializers.IntegerField(source='author.pk', required=False)
    author_username = serializers.CharField(source='author.username', required=False)
    class Meta:
        model = Blog
        fields = (
            'url', 'pk', 'title', 'author_url', 'author_pk', 'author_username', 'body', 'date_created', 'date_modified', 'comments_url',
        )
    
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author_url = serializers.HyperlinkedRelatedField(view_name='user-detail', source='author', read_only=True)
    author_pk = serializers.IntegerField(source='author.pk', required=False)
    author_username = serializers.CharField(source='author.username', required=False)
    blog_url = serializers.HyperlinkedRelatedField(view_name='blog-detail', source='blog', read_only=True)
    class Meta:
        model = Comment
        fields = (
            'url',
            'pk',
            'author_url',
            'blog_url',
            'body',
            'author_pk',
            'author_username',
        )