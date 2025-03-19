from django.contrib.auth import views as auth_views
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentListView, CommentCreateView, CommentUpdateView, CommentDeleteView


urlpatterns = [
    # Built-in login/logout views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Custom registration view
    path('register/', views.register, name='register'),

    # Profile page (to be implemented later)
    path('profile/', views.profile, name='profile'),

    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('post/<int:post_id>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:post_id>/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:post_id>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




