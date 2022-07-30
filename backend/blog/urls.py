from django.urls import path

from . import views

urlpatterns = [
    # Blog
    path('v1/', views.BlogList.as_view(), name='blog-list'),
    path('v1/<int:pk>/', views.BlogDetail.as_view(), name='blog-detail'),
    
    # Comments
    path('v1/<int:pk>/comments/', views.BlogCommentList.as_view(), name='blog-comment-list'),
    path('v1/comment/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
]
