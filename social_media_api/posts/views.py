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
    

class LikePostView(generics.GenericAPIView):
    """Allows an authenticated user to like a post."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """Handles post liking."""
        post = generics.get_object_or_404(Post, pk=pk)  # Ensure post exists
        like, created = Like.objects.get_or_create(author=request.user, post=post)  # Like post

        if created:
            # Create a notification for the post owner
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post"
            )
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)

        return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(generics.GenericAPIView):
    """Allows an authenticated user to unlike a post."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        """Handles post unliking."""
        post = generics.get_object_or_404(Post, pk=pk)  # Ensure post exists
        like = Like.objects.filter(author=request.user, post=post)  # Check if user liked

        if like.exists():
            like.delete()  # Unlike the post
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)