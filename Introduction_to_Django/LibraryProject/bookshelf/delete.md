Python command
book = Book.objects.get(id=4)
book.delete()
(1, {'bookshelf.Book': 1})

Confirming the Delete
Book.objects.all()           
<QuerySet []>