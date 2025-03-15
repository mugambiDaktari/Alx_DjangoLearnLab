from django.test import TestCase
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class BookAPITestCase(APITestCase):
    """Tests CRUD, filtering, searching, and ordering for the Book API"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create an author
        self.author = Author.objects.create(name="John Doe")

        # Create books
        self.book1 = Book.objects.create(title="Python Basics", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Advanced Django", publication_year=2021, author=self.author)

        self.book_url = "/api/books/"

    # Test: Creating a Book (POST)
    def test_create_book(self):
        """Ensure a book can be created via the API"""
        self.client.login(username="testuser", password="password123")  # Authenticate user
        data = {"title": "Machine Learning", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(self.book_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # Test: Retrieving Books (GET)
    def test_list_books(self):
        """Ensure books can be retrieved"""
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test: Retrieving a Single Book (GET /books/<id>/)
    def test_retrieve_book(self):
        """Ensure a single book can be retrieved"""
        response = self.client.get(f"{self.book_url}{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # Test: Updating a Book (PUT)
    def test_update_book(self):
        """Ensure a book can be updated"""
        self.client.login(username="testuser", password="password123")  # Authenticate user
        updated_data = {"title": "Updated Python Basics", "publication_year": 2020, "author": self.author.id}
        response = self.client.put(f"{self.book_url}{self.book1.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Python Basics")

    # Test: Deleting a Book (DELETE)
    def test_delete_book(self):
        """Ensure a book can be deleted"""
        self.client.login(username="testuser", password="password123")  # Authenticate user
        response = self.client.delete(f"{self.book_url}{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # Test: Filtering Books by Title
    def test_filter_books_by_title(self):
        """Ensure books can be filtered by title"""
        response = self.client.get(f"{self.book_url}?title=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test: Searching Books by Title
    def test_search_books(self):
        """Ensure books can be searched"""
        response = self.client.get(f"{self.book_url}?search=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test: Ordering Books by Publication Year (Ascending)
    def test_order_books_by_publication_year(self):
        """Ensure books can be ordered by publication year"""
        response = self.client.get(f"{self.book_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Python Basics")

    # Test: Checking Permissions (Unauthenticated User)
    def test_unauthorized_user_cannot_create_book(self):
        """Ensure unauthorized users cannot create books"""
        data = {"title": "Unauthorized Book", "publication_year": 2023, "author": self.author.id}
        response = self.client.post(self.book_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)