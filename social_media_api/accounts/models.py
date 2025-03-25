from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def __str__(self):
        return self.username