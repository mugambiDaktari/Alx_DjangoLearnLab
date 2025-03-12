from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListViews.as_view(), name='book-list'), # shows all books
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),# shows a specific book
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),# creates a new book
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),# updates a book
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),# deletes a book
    """ path('authors/', views.AuthorListViews.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/update/<int:pk>/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/delete/<int:pk>/', views.AuthorDeleteView.as_view(), name='author-delete'), """
]