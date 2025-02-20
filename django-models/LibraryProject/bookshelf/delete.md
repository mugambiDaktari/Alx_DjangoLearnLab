Python command
book = Book.objects.get(id=4)
book.delete()
(1, {'bookshelf.Book': 1})

Confirming the Delete
from bookshelf.models import Book
Book.objects.all()           
<QuerySet []>