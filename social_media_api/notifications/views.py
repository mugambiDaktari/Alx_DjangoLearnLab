from rest_framework import generics, permissions
from rest_framework.response import Response
from notifications.models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user).order_by('is_read', '-timestamp')

class MarkNotificationReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient != request.user:
            return Response({"error": "You cannot mark this notification"}, status=status.HTTP_403_FORBIDDEN)
        
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})

