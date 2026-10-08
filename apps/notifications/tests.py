from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile
from apps.notifications.models import Notification, NotificationPreference

User = get_user_model()

class NotificationEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="notif_student@example.com", username="nstudent", password="Password123!")
        self.profile = StudentProfile.objects.create(user=self.user, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.n1 = Notification.objects.create(
            student=self.profile,
            type="RECOMMENDATION_NEW",
            title="New Course Recommendation",
            message="Check out Andrew Ng Machine Learning course!",
            is_read=False
        )
        self.n2 = Notification.objects.create(
            student=self.profile,
            type="SKILL_DECAY_WARNING",
            title="Skill Assessment Reminder",
            message="Your Python skill assessment is due.",
            is_read=False
        )

    def test_list_notifications_and_unread_count(self):
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['unread_count'], 2)
        self.assertEqual(len(response.data['data']['notifications']), 2)

    def test_mark_single_notification_read(self):
        url = reverse('notification-read', kwargs={'pk': str(self.n1.id)})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['data']['is_read'])
        
        self.n1.refresh_from_db()
        self.assertTrue(self.n1.is_read)

    def test_mark_all_notifications_read(self):
        url = reverse('notification-read-all')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.filter(student=self.profile, is_read=False).count(), 0)
