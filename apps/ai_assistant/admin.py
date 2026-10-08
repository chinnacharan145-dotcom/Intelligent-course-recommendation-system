from django.contrib import admin
from .models import AIConversation, AIMessage, AIObservabilityLog

class AIMessageInline(admin.TabularInline):
    model = AIMessage
    extra = 1

@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'created_at', 'updated_at')
    search_fields = ('title', 'student__user__email')
    inlines = [AIMessageInline]

@admin.register(AIObservabilityLog)
class AIObservabilityLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'conversation', 'prompt_tokens', 'completion_tokens', 'response_latency_ms', 'safety_flagged', 'created_at')
    list_filter = ('model_name', 'safety_flagged', 'created_at')
