from django.shortcuts import render
from .models import Author, Book, Library, Librarian
from django.views.generic import DetailView, ListView


# Create your views here
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'