from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Notification
from .serializers import NotificationSerializer


class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer    = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class MarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.delete()
            return Response({'message': 'Deleted'}, status=204)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)


class MarkAllReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})