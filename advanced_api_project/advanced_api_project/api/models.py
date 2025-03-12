from django.db import models  # Import Django's ORM models

# Create your models here.

class Author(models.Model):
    """
    Represents an author in the database.
    
    Fields:
    - `name`: Stores the author's full name (max 100 characters).
    - `email`: Stores the author's email address (must be unique and valid).
    - `active`: Boolean field to indicate if the author is active (default: False).
    - `created_on`: Stores the date and time when the author was created (auto-generated).
    - `last_logged_in`: Updates automatically whenever the author logs in.
    """

    name = models.CharField(max_length=100)  # Stores the author's name (max length: 100)
    email = models.EmailField()  # Stores the author's email (ensures proper email format)
    active = models.BooleanField(default=False)  # Indicates whether the author is active
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically sets the date/time when the author is created
    last_logged_in = models.DateTimeField(auto_now=True)  # Updates to the current time whenever the author logs in

    def __str__(self):
        """
        String representation of the Author model.
        - Returns the author's name when the object is printed.
        """
        return self.name


class Book(models.Model):
    """
    Represents a book in the database.
    
    Fields:
    - `title`: The title of the book (max 100 characters).
    - `publication_year`: The year the book was published (integer).
    - `author`: ForeignKey linking to the Author model (one-to-many relationship).
        - `on_delete=models.CASCADE`: If an author is deleted, all their books are also deleted.
        - `related_name='books'`: Allows reverse lookup from the Author model (e.g., `author.books.all()`).
    """

    title = models.CharField(max_length=100)  # Stores the book title (max length: 100)
    publication_year = models.IntegerField()  # Stores the year the book was published
    author = models.ForeignKey(
        Author,  # Links each book to an author
        on_delete=models.CASCADE,  # Deletes all books if the author is deleted
        related_name='books'  # Enables reverse lookup (e.g., `author.books.all()`)
    )

    def __str__(self):
        """
        String representation of the Book model.
        - Returns the book title when the object is printed.
        """
        return self.title
