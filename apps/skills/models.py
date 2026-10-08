import uuid
from django.db import models

class SkillCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(SkillCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='skills')
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SkillPrerequisite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='prerequisites')
    prerequisite_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='required_for_skills')
    minimum_level = models.IntegerField(default=40)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ('skill', 'prerequisite_skill')

    def __str__(self):
        return f"{self.skill.name} requires {self.prerequisite_skill.name} (Min Level: {self.minimum_level})"


class Interest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
