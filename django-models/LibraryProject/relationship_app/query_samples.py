from relationship_app.models import Book, Author, Library, Librarian

# Query all books by a specific author.
books_by_author = Book.objects.filter(author__name="Author's Name")

# List all books in a library.
library = Library.objects.get(name="Library Name")
books_in_library = library.books.all()

# Retrieve the librarian for a library.
library = Library.objects.get(name="Library Name")
librarian = library.librarian