from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Post, Comment, Like

User = get_user_model() 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Comment.objects.create(author=self.context['request'].user, **validated_data)
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.IntegerField(source='likes_count', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'comments', 'likes', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Post.objects.create(author=self.context['request'].user, **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['author']  # Prevent users from setting the author themselves

from rest_framework import serializers
from .models import Like



