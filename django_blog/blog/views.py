from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Your account has been created successfully!')
            return redirect('profile')  # Redirect to profile or home page
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/profile.html', context)

# List View - Display all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Template to use
    context_object_name = 'posts'
    ordering = ['-published_date']  # Show latest posts first

# Detail View - Display single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Template to use

# Create View - Allow users to create new posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'  # Template to use

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign logged-in user as author
        return super().form_valid(form)

# Update View - Allow authors to edit their own posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Allow only the author to edit

# Delete View - Allow authors to delete their own posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Allow only the author to delete

class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comment_list.html'  
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id']).order_by('-created_at')