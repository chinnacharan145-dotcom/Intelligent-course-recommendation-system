import uuid
from django.db import models
from apps.skills.models import Skill

class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Course Categories"

    def __str__(self):
        return self.name


class CourseProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = 'Beginner', 'Beginner'
        INTERMEDIATE = 'Intermediate', 'Intermediate'
        ADVANCED = 'Advanced', 'Advanced'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    provider = models.ForeignKey(CourseProvider, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    difficulty = models.CharField(max_length=50, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    duration_hours = models.DecimalField(max_digits=6, decimal_places=2, default=20.00)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.50)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    is_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.provider.name if self.provider else 'Direct'})"


class CourseSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='course_mappings')
    level = models.IntegerField(default=50, help_text="Skill level taught 0-100")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'skill')

    def __str__(self):
        return f"{self.course.title} -> Teaches {self.skill.name} (Level: {self.level})"


class CoursePrerequisite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisites')
    required_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='prerequisite_courses')
    minimum_level = models.IntegerField(default=40, help_text="Minimum proficiency 0-100")
    is_mandatory = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'required_skill')

    def __str__(self):
        return f"{self.course.title} requires {self.required_skill.name} (Min Level: {self.minimum_level})"
