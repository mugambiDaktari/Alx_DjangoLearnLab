 Python command

book = Book.objects.get(title="1984")
book.title =  "Nineteen Eighty-Four" 
book.save()

updated title.
Book.objects.get(id=1)
<Book: Nineteen Eighty-Four by George Orwell (1949)>