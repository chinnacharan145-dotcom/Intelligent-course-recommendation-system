from django.contrib import admin
from .models import Notification, NotificationPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'type', 'priority', 'is_read', 'created_at')
    list_filter = ('type', 'priority', 'is_read')
    search_fields = ('title', 'message', 'student__user__email')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment_notifications', 'skill_notifications', 'career_notifications', 'course_notifications')
