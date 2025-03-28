from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import CustomUser  # Ensure this is the correct import

User = get_user_model()

class FollowSerializer(serializers.Serializer):
    following_user_id = serializers.IntegerField()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Ensure this is the correct model
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['followers']  # Make followers read-only

    def create(self, validated_data):
        user = get_user_model().objects.create_user( 
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
        )
        Token.objects.create(user=user)  # Generate token for new user
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']
        extra_kwargs = {'password': {'write_only': True}}
 
    def create(self, validated_data):
        #Creates a user and ensures password is hashed.
        user = User.objects.create_user(  # Explicitly calling create_user()
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
        )
        Token.objects.create(user=user)  # Generate token for new user
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    """
