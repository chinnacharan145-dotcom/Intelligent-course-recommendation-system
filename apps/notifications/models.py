import uuid
from django.db import models
from apps.students.models import StudentProfile

class Notification(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.student.user.email}: {self.title}"


class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='notification_preferences')
    assessment_notifications = models.BooleanField(default=True)
    skill_notifications = models.BooleanField(default=True)
    career_notifications = models.BooleanField(default=True)
    course_notifications = models.BooleanField(default=True)
    recommendation_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification Preferences for {self.student.user.email}"
