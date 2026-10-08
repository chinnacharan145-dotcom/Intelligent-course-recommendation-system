import uuid
from django.db import models
from apps.students.models import StudentProfile
from apps.courses.models import Course
from apps.careers.models import Career

class Recommendation(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DISMISSED = 'DISMISSED', 'Dismissed'
        COMPLETED = 'COMPLETED', 'Completed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='recommendations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='recommendations')
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommendations')
    
    match_score = models.DecimalField(max_digits=5, decimal_places=2)
    career_match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skill_match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interest_match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    branch_match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    semester_match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    difficulty_match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    content_similarity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE)
    generated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-match_score']

    def __str__(self):
        return f"Rec for {self.student.user.email}: {self.course.title} ({self.match_score}%)"


class RecommendationReason(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='reasons')
    reason_type = models.CharField(max_length=50)
    reason_text = models.TextField()
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"Reason ({self.reason_type}): {self.reason_text[:40]}"


class RecommendationFeedback(models.Model):
    class FeedbackType(models.TextChoices):
        INTERESTED = 'INTERESTED', 'Interested'
        NOT_INTERESTED = 'NOT_INTERESTED', 'Not Interested'
        ALREADY_KNOW = 'ALREADY_KNOW', 'Already Know This'
        TOO_EASY = 'TOO_EASY', 'Too Easy'
        TOO_HARD = 'TOO_HARD', 'Too Hard'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='recommendation_feedbacks')
    feedback_type = models.CharField(max_length=50, choices=FeedbackType.choices)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.feedback_type} by {self.student.user.email} on {self.recommendation.course.title}"
