from rest_framework import filters, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Blog, Comment
from .permissions import IsOwnerOrReadOnly, ReadOnly
from .serializers import BlogSerializer, CommentSerializer

class BlogList(generics.ListCreateAPIView):
    """
    GET     - List of blogs
    POST    - Create blog
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body', 'author__email', 'author__username']

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET     - Return blog
    PUT     - Update blog if owner
    DELETE  - Delete blog if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser, FormParser)

class BlogCommentList(generics.ListCreateAPIView):
    """
    GET     - List of comments belonging to the blog
    POST    - Create comment for blog
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['body', 'author__username']
    def get_queryset(self):
        try:
            return Comment.objects.filter(blog__pk = self.kwargs['pk'])
        except Exception:
            return []
    
    def perform_create(self, serializer):
        blog_id = self.kwargs['pk']
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            raise Exception("Blog with given id does not exist")
        Comment.objects.create(
            author=self.request.user,
            blog=blog,
            body=self.request.data['body']
        )

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET     - Return comments
    PUT     - Update comment
    DELETE  - Delete comment
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()