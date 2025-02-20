from relationship_app.models import Book, Author, Library, Librarian

# Query all books by a specific author.
author_name = "Author's Name"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)

# List all books in a library.
library_name = "Library_name"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()


# Retrieve the librarian for a library.
library = Library.objects.get(name=library_name)
librarian = library.librarian