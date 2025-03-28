from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)  # To track unread notifications
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Store model type
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')  # Generic foreign key
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.actor} {self.verb} {self.recipient}'