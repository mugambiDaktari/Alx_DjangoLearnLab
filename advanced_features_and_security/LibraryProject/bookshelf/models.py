from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Book(models.Model):
       title = models.CharField(max_length=200)
       author = models.CharField(max_length=100)
       publication_year = models.IntegerField()

       def __str__(self):
             return f"{self.title} by {self.author} ({self.publication_year})"