from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from rest_framework import generics, permissions

from notifications.models import Notification # Import the Notification model
from django.shortcuts import get_object_or_404


from django.views.generic import TemplateView
from django.contrib.auth import get_user_model


User = get_user_model()

class HomePageView(TemplateView):
    template_name = "posts/homepage.html"


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
        """   def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer) """
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommentPostView(generics.CreateAPIView):
    """✅ Comment on a post and create a notification"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('post_id')
        post = Post.objects.filter(id=post_id).first()

        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(author=user, post=post, text=request.data['text'])

        # Generate a notification if the commenter is not the post owner
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="commented on your post"
            )

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()  # Get users the current user follows
        return Post.objects.filter(author__in=following_users).order_by('-created_at')  # Get posts from those users that the current user follows
    

from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.models import ContentType

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)  # Ensure post exists

        # Prevent users from liking their own posts
        if post.author == request.user:
            return Response({"error": "You cannot like your own post."}, status=status.HTTP_400_BAD_REQUEST)

        like, created = Like.objects.get_or_create(user=request.user, post=post) 

        if created:
            # Create a notification for the post owner
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.id
            )
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)

        return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.GenericAPIView):
    """Allows an authenticated user to unlike a post."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        """Handles post unliking."""
        post = generics.get_object_or_404(Post, pk=pk)  # Ensure post exists
        like = Like.objects.filter(user=request.user, post=post)  # Fix: Use 'user' field

        if like.exists():
            like.delete()  # Unlike the post
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
