from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer
from apps.students.models import StudentProfile

class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        unread_only = request.query_params.get('unread', 'false').lower() in ('true', '1')

        notifications_qs = Notification.objects.filter(student=profile)
        if unread_only:
            notifications_qs = notifications_qs.filter(is_read=False)

        unread_count = Notification.objects.filter(student=profile, is_read=False).count()
        serializer = NotificationSerializer(notifications_qs[:20], many=True)

        return Response({
            "success": True,
            "data": {
                "unread_count": unread_count,
                "notifications": serializer.data
            },
            "message": None
        })


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        notification = get_object_or_404(Notification, pk=pk, student=profile)

        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

        return Response({
            "success": True,
            "data": NotificationSerializer(notification).data,
            "message": "Notification marked as read."
        })


class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        Notification.objects.filter(student=profile, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({
            "success": True,
            "message": "All notifications marked as read."
        })


class NotificationPreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        pref, _ = NotificationPreference.objects.get_or_create(student=profile)
        serializer = NotificationPreferenceSerializer(pref)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

    def patch(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        pref, _ = NotificationPreference.objects.get_or_create(student=profile)
        serializer = NotificationPreferenceSerializer(pref, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Notification preferences updated."
        })
