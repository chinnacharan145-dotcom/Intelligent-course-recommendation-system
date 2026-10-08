import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.academics.models import University, College, Branch, Regulation
from apps.skills.models import Skill, Interest
from apps.careers.models import Career

User = get_user_model()

class StudentProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    regulation = models.ForeignKey(Regulation, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    current_semester = models.IntegerField(default=1)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=8.00)
    weekly_learning_hours = models.IntegerField(default=10)
    onboarding_completed = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.email}"


class StudentInterest(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='interests')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='interested_students')
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.HIGH)
    interest_level = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'interest')

    def __str__(self):
        return f"{self.student.user.email} -> {self.interest.name}"


class StudentCareerGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='career_goals')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='aspiring_students')
    priority = models.IntegerField(default=1)
    is_primary = models.BooleanField(default=True)
    target_semester = models.IntegerField(default=8)
    target_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.email} -> Goal: {self.career.name}"


class StudentSkill(models.Model):
    class SourceChoice(models.TextChoices):
        SELF_ASSESSMENT = 'SELF_ASSESSMENT', 'Self Assessment'
        SELF_DECLARED = 'SELF_DECLARED', 'Self Declared'
        ASSESSMENT_RESULT = 'ASSESSMENT_RESULT', 'Assessment Result'
        COURSE_COMPLETION = 'COURSE_COMPLETION', 'Course Completion'
        MANUAL_OVERRIDE = 'MANUAL_OVERRIDE', 'Manual Override'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_skills')
    proficiency = models.IntegerField(default=0)
    confidence = models.FloatField(default=0.50)
    source = models.CharField(max_length=50, choices=SourceChoice.choices, default=SourceChoice.SELF_ASSESSMENT)
    last_assessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.email} - {self.skill.name}: Level {self.proficiency}"


class StudentSkillHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skill_history')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_history')
    old_proficiency = models.IntegerField()
    new_proficiency = models.IntegerField()
    change_source = models.CharField(max_length=50)
    reference_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History {self.student.user.email} {self.skill.name}: {self.old_proficiency} -> {self.new_proficiency}"
