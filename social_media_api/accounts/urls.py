from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('follow/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    # path('followers/<str:username>/', FollowersListView.as_view(), name='followers-list'),
    # path('following/<str:username>/', FollowingListView.as_view(), name='following-list'),
]