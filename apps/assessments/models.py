import uuid
from django.db import models
from apps.skills.models import Skill
from apps.students.models import StudentProfile

class Assessment(models.Model):
    class Type(models.TextChoices):
        DIAGNOSTIC = 'DIAGNOSTIC', 'Diagnostic Assessment'
        SKILL_LEVEL = 'SKILL_LEVEL', 'Skill Level Test'
        MODULE_QUIZ = 'MODULE_QUIZ', 'Module Quiz'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assessment_type = models.CharField(max_length=50, choices=Type.choices, default=Type.SKILL_LEVEL)
    duration_minutes = models.IntegerField(default=30)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AssessmentQuestion(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = 'Beginner', 'Beginner'
        INTERMEDIATE = 'Intermediate', 'Intermediate'
        ADVANCED = 'Advanced', 'Advanced'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    skill = models.ForeignKey(Skill, on_delete=models.RESTRICT, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, default='MCQ')
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    difficulty = models.CharField(max_length=50, choices=Difficulty.choices, default=Difficulty.INTERMEDIATE)
    question_order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question_order']

    def __str__(self):
        return f"{self.assessment.title} Q{self.question_order}: {self.question_text[:40]}"


class AssessmentOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    option_order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['option_order']

    def __str__(self):
        return f"{self.question.question_text[:20]} -> {self.option_text}"


class AssessmentAttempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        EVALUATED = 'EVALUATED', 'Evaluated'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.IN_PROGRESS)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attempt by {self.student.user.email} on {self.assessment.title} ({self.status})"


class StudentAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE, related_name='student_answers')
    selected_option = models.ForeignKey(AssessmentOption, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"Answer for attempt {self.attempt.id} Q: {self.question.question_text[:20]}"


class AssessmentResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.OneToOneField(AssessmentAttempt, on_delete=models.CASCADE, related_name='result')
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    incorrect_answers = models.IntegerField()
    unanswered = models.IntegerField()
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    skill_level = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for Attempt {self.attempt.id}: {self.percentage}%"


class AssessmentSkillResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment_result = models.ForeignKey(AssessmentResult, on_delete=models.CASCADE, related_name='skill_results')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assessment_results')
    questions_count = models.IntegerField()
    correct_count = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    skill_score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assessment_result', 'skill')

    def __str__(self):
        return f"Skill Result {self.skill.name}: {self.percentage}%"
