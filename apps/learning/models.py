import uuid
from django.db import models
from apps.students.models import StudentProfile
from apps.courses.models import Course

class StudentCourse(models.Model):
    class Status(models.TextChoices):
        SAVED = 'SAVED', 'Saved'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        DROPPED = 'DROPPED', 'Dropped'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.IN_PROGRESS)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.email} -> {self.course.title} ({self.status}: {self.progress}%)"


class LearningActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='activities')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    activity_type = models.CharField(max_length=50)
    duration_minutes = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Activity {self.activity_type} by {self.student.user.email} ({self.duration_minutes} mins)"
