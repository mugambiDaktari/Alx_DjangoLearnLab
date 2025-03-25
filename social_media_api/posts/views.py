from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from rest_framework import generics, permissions

from notifications.models import Notification # Import the Notification model




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
    
class LikePostView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('post_id')

        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if Like.objects.filter(author=user, post=post).exists():
            return Response({"error": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like = Like.objects.create(author=user, post=post)

        # Generate a notification if the liker is not the post owner
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked your post"
            )

        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('post_id')

        # Check if the like exists
        like = Like.objects.filter(author=user, post_id=post_id).first()
        if not like:
            return Response({"error": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()  # Remove like

        # Delete the notification
        Notification.objects.filter(
            recipient=like.post.author,
            actor=user,
            verb="liked your post"
        ).delete()

        return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)