from django.urls import path
from .views import list_books, LibraryDetailView, add_book_view, edit_book_view, delete_book_view   
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from . import views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    path('signup/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    path('add_book/', add_book_view, name='add_book'),

    path('edit_book/<int:book_id>/', edit_book_view, name='edit_book'),

    path('delete_book/<int:book_id>/', delete_book_view, name='delete_book'),
]