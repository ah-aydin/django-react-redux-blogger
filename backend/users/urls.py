from django.urls import path
from . import views

urlpatterns = [
    # List
    path('v1/', views.UserList.as_view(), name='user-list'),
    # Detail
    path('v1/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    # Follow account
    path('v1/<int:pk>/follow/', views.CreateDestoryFollow.as_view(), name='user-create-destory-follow'),
    path('v1/<int:pk>/follows/', views.UserFollows.as_view(), name='user-follows-list'),
    path('v1/<int:pk>/followers/', views.UserFollowers.as_view(), name='user-followers-list'),
    # Activate
    path('v1/activate/<uid64>/<token>/', views.activateUser, name='user-activate'),
    # Reset password
    path('v1/password_reset/request/', views.requestResetPassword, name='user-reset-password-request'),
    path('v1/password_reset/<uid64>/<token>/', views.resetPassword, name='user-reset-password'),
]
