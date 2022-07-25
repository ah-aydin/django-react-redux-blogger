from django.urls import path
from . import views

urlpatterns = [
    # List
    path('v1/', views.UserList.as_view(), name='user-list'),
    # Detail
    path('v1/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    # Activate
    path('v1/activate/<uidb64>/<token>/', views.activateUser, name='user-activate'),
]
