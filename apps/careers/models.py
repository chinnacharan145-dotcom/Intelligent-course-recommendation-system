import uuid
from django.db import models
from apps.skills.models import Skill

class Career(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, default='Software & Technology')
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    job_outlook = models.TextField(blank=True, null=True)
    typical_roles = models.JSONField(default=list, blank=True)
    education_requirements = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CareerSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='required_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='career_mappings')
    required_level = models.IntegerField(default=70, help_text="Target proficiency level 0-100")
    importance = models.IntegerField(default=3, help_text="Importance rating 1-5")
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('career', 'skill')

    def __str__(self):
        return f"{self.career.name} -> {self.skill.name} (Req Level: {self.required_level})"


class CareerReadinessSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='readiness_snapshots')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='readiness_snapshots')
    readiness_score = models.DecimalField(max_digits=5, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-calculated_at']

    def __str__(self):
        return f"Snapshot {self.student.user.email} -> {self.career.name}: {self.readiness_score}%"


class SkillGapSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='skill_gap_snapshots')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='skill_gap_snapshots')
    total_gaps_count = models.IntegerField()
    avg_gap_size = models.DecimalField(max_digits=5, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-calculated_at']

    def __str__(self):
        return f"Skill Gap Snapshot {self.student.user.email}: {self.total_gaps_count} Gaps"
