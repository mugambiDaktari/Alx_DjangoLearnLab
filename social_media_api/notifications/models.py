from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)  # To track unread notifications
    target = models.GenericForeignKey()  # To store the target object of the notification
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.actor} {self.verb} {self.recipient}'