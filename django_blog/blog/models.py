from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from taggit.managers import TaggableManager  # Import django-taggit


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(default=now) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50] 
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    about = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name