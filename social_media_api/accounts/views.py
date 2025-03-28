from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer, FollowSerializer
from django.shortcuts import get_object_or_404
from .models import CustomUser 

from notifications.models import Notification
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": response.data}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id, "username": user.username})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Ensure users can only access their own profile\
    
class FollowUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):
        """ Allows an authenticated user to follow another user. """
        user = request.user
        following_user_id = request.data.get('following_user_id')

        if not following_user_id:
            return Response({"error": "Following user ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        following_user = get_object_or_404(User, id=following_user_id)

        if user == following_user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if user.following.filter(id=following_user.id).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        user.following.add(following_user)

        return Response({
            "message": f"You are now following {following_user.username}.",
            "follower_count": following_user.followers.count()
        }, status=status.HTTP_200_OK)
class UnfollowUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, username, *args, **kwargs):
        user_to_unfollow = get_object_or_404(User, username=username)
        user = request.user

        if user == user_to_unfollow:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_unfollow not in user.following.all():
            return Response({"error": f"You are not following {username}."}, status=status.HTTP_400_BAD_REQUEST)

        user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {username}."}, status=status.HTTP_200_OK)
    