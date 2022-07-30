from ast import excepthandler
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
import json

from .models import Follow, User
from .serializers import UserCreateSerializer, UserSerializer, UserCreateResponseSerializer, UserFollowerSerializer, FollowingSerializer
from .utils.user_status import activate_user, reset_password
from .utils.email import send_activation_email, send_password_reset_email

class UserList(generics.ListCreateAPIView):
    queryset = User.fetchAll(User)
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'username']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        if self.request.method == 'POST':
            return UserCreateSerializer
    
    def create(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        re_password = request.data['re_password']
        
        if password != re_password:
            return Response({"error": "Passwords do not match"}, status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(email, username, password)
        except Exception:
            return Response({"error": "User with the given username and/or email allready exists"}, status.HTTP_400_BAD_REQUEST)
        
        try:
            send_activation_email(request, user)
        except Exception:
            user.delete()
            return Response({"error": "Failed to send activation email"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Return the created user
        serializer = UserCreateResponseSerializer(request.data)
        return Response(serializer.data, status.HTTP_201_CREATED)
            
    def _check_passwords(self, data):
        return data['re_password'] != data['password']

class UserDetail(generics.RetrieveAPIView):
    queryset = User.fetchAll(User)
    serializer_class = UserSerializer

@require_http_methods(['GET'])
def activateUser(request, uid64, token):
    if activate_user(uid64, token):
        return JsonResponse({"successfull": True})
    return JsonResponse({"successfull": False})

@csrf_exempt
@require_http_methods(['POST'])
def requestResetPassword(request):
    try:
        JSON = json.loads(request.body)
    except:
        return JsonResponse({"successfull": False})
    
    email = JSON['email']
    try:
        send_password_reset_email(request, email)
        return JsonResponse({"successfull": True})
    except:
        return JsonResponse({"successfull": False})

@csrf_exempt
@require_http_methods(['POST'])
def resetPassword(request, uid64, token):
    try:
        JSON = json.loads(request.body)
    except:
        return JsonResponse({"successfull": False})
    
    password = JSON['password']
    re_password = JSON['re_password']
    if password != re_password:
        return JsonResponse({"error": "Passwords do not match"})
    if reset_password(uid64, token, password):
        return JsonResponse({"successfull": True})
    return JsonResponse({"successfull": False})

class CreateDestoryFollow(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        # Check if account exists
        user_to_follow_id = pk
        try:
            follows = User.objects.get(pk=user_to_follow_id)
        except User.DoesNotExist:
            return Response({"error": f"No user with id {user_to_follow_id}"})
    
        # Check if the authenticated user is allready following this person or not
        try:
            # Remove the follow
            follow = Follow.objects.get(follower=request.user, follows=follows)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            # Create new follow
            follow = Follow.objects.create(follower=request.user, follows=follows)
            return Response("followed", status=status.HTTP_201_CREATED)

class UserFollowers(generics.ListAPIView):
    """
    List of followers of the user
    """
    serializer_class = UserFollowerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['follower__email', 'follower__username']
    def get_queryset(self):
        try:
            return Follow.objects.filter(follows__pk=self.kwargs['pk']).order_by('follower__username')
        except:
            return []

class UserFollows(generics.ListAPIView):
    """
    List of users the user follows
    """
    serializer_class = FollowingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['follows__email', 'follows__username']
    def get_queryset(self):
        try:
            return Follow.objects.filter(follower__pk=self.kwargs['pk']).order_by('follows__username')
        except:
            return []
