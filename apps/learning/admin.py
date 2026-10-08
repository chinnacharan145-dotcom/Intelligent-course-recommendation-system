from django.contrib import admin
from .models import StudentCourse, LearningActivity

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'progress', 'started_at', 'completed_at', 'last_accessed')
    list_filter = ('status',)
    search_fields = ('student__user__email', 'course__title')

@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'activity_type', 'duration_minutes', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('student__user__email', 'course__title')
