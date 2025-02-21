from django.shortcuts import render, redirect
from .models import Book 
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

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

@user_passes_test(user_is_admin)
def admin_view(request):
    # View logic for Admin
    return render(request, 'relationship_app/admin_view.html')

@librarian_required
def librarian_view(request):
    # View logic for Librarian
    return render(request, 'relationship_app/librarian_view.html')

@member_required
def member_view(request):
    # View logic for Member
    return render(request, 'relationship_app/member_view.html')


