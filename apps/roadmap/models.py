import uuid
from django.db import models
from apps.students.models import StudentProfile
from apps.careers.models import Career
from apps.skills.models import Skill

class Roadmap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='roadmaps')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    overall_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Roadmap: {self.title} for {self.student.user.email}"


class RoadmapNode(models.Model):
    class NodeType(models.TextChoices):
        SKILL = 'SKILL', 'Skill Node'
        ASSESSMENT = 'ASSESSMENT', 'Assessment Milestone'
        PROJECT = 'PROJECT', 'Project Milestone'

    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='nodes')
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='roadmap_nodes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    node_type = models.CharField(max_length=50, choices=NodeType.choices, default=NodeType.SKILL)
    sequence_order = models.IntegerField()
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.NOT_STARTED)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sequence_order']

    def __str__(self):
        return f"Node {self.sequence_order}: {self.title} ({self.status})"


class RoadmapNodeSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roadmap_node = models.ForeignKey(RoadmapNode, on_delete=models.CASCADE, related_name='node_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='node_mappings')
    target_level = models.IntegerField(default=70)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('roadmap_node', 'skill')

    def __str__(self):
        return f"{self.roadmap_node.title} -> {self.skill.name} (Target: {self.target_level})"


class Action(models.Model):
    class ActionType(models.TextChoices):
        ASSESSMENT = 'ASSESSMENT', 'Take Skill Assessment'
        COURSE_START = 'COURSE_START', 'Start Prerequisite Course'
        COURSE_CONTINUE = 'COURSE_CONTINUE', 'Continue In-Progress Course'
        ROADMAP_NODE = 'ROADMAP_NODE', 'Complete Roadmap Node'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_type = models.CharField(max_length=50, choices=ActionType.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority_weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action Template: {self.title} ({self.action_type})"


class StudentAction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Action'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        DISMISSED = 'DISMISSED', 'Dismissed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='next_best_actions')
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='student_assignments')
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.UUIDField(null=True, blank=True)
    priority_score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    generated_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Next Action for {self.student.user.email}: {self.action.title} (Priority: {self.priority_score})"


class StudentActionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_action = models.ForeignKey(StudentAction, on_delete=models.CASCADE, related_name='history')
    previous_status = models.CharField(max_length=50, blank=True, null=True)
    new_status = models.CharField(max_length=50)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action Audit #{self.id}: {self.previous_status} -> {self.new_status}"
