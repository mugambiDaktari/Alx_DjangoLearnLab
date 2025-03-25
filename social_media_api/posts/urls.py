from django.urls import path
from .views import PostViewSet, CommentViewSet, FeedView

urlpatterns = [
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts'),
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 
        'patch': 'partial_update', 'delete': 'destroy'}), name='post'),
    path('comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 
        'patch': 'partial_update', 'delete': 'destroy'}), name='comment'),

    path('feed/', FeedView.as_view(), name='feed'),
]