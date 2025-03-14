from django.shortcuts import render, redirect
from .models import Book 
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required


# Create your views here
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def user_is_admin(user):
    if user.userprofile.role == 'Admin':
        return True
    raise PermissionDenied

def user_is_librarian(user):
    if user.userprofile.role == 'Librarian':
        return True
    raise PermissionDenied

def user_is_member(user):
    if user.userprofile.role == 'Member':
        return True
    raise PermissionDenied

@user_passes_test(user_is_admin)
def admin_view(request):
    # View logic for Admin
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(user_is_librarian)
def librarian_view(request):
    # View logic for Admin
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(user_is_member)
def member_view(request):
    # View logic for Admin
    return render(request, 'relationship_app/member_view.html')

@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title and author:  # Basic validation
            Book.objects.create(title=title, author=author)
            return redirect('book_list')  # Redirect after adding
    return render(request, 'books/add_book.html')

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title and author:
            book.title = title
            book.author = author
            book.save()
            return redirect('book_list')  # Redirect after editing
    return render(request, 'books/edit_book.html', {'book': book})

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect after deleting
    return render(request, 'books/delete_book.html', {'book': book})