from django.contrib import admin
from .models import AnalyticsEvent

@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'student', 'ip_address', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('event_type', 'student__user__email')
