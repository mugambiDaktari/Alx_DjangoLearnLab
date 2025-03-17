from django.contrib.auth import views as auth_views
from django.urls import path
from . import views  

urlpatterns = [
    # Built-in login/logout views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Custom registration view
    path('register/', views.register, name='register'),

    # Profile page (to be implemented later)
    path('profile/', views.profile, name='profile'),
]
