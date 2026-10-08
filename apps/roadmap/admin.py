from django.contrib import admin
from .models import Roadmap, RoadmapNode, RoadmapNodeSkill, Action, StudentAction, StudentActionHistory

class RoadmapNodeInline(admin.TabularInline):
    model = RoadmapNode
    extra = 1

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'career', 'overall_progress', 'status', 'created_at')
    list_filter = ('status', 'career')
    search_fields = ('title', 'student__user__email')
    inlines = [RoadmapNodeInline]

@admin.register(RoadmapNode)
class RoadmapNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'roadmap', 'skill', 'node_type', 'sequence_order', 'status', 'progress')
    list_filter = ('node_type', 'status')

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'action_type', 'priority_weight', 'is_active')
    list_filter = ('action_type', 'is_active')

@admin.register(StudentAction)
class StudentActionAdmin(admin.ModelAdmin):
    list_display = ('student', 'action', 'priority_score', 'status', 'generated_at')
    list_filter = ('status',)

@admin.register(StudentActionHistory)
class StudentActionHistoryAdmin(admin.ModelAdmin):
    list_display = ('student_action', 'previous_status', 'new_status', 'changed_at')
