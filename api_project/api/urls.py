from .views import BookViewSet, BookList
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')


urlpatterns = [
     path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]