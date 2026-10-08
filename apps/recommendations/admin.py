from django.contrib import admin
from .models import Recommendation, RecommendationReason, RecommendationFeedback

class RecommendationReasonInline(admin.TabularInline):
    model = RecommendationReason
    extra = 1

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'career', 'match_score', 'status', 'generated_at')
    list_filter = ('status', 'generated_at')
    search_fields = ('student__user__email', 'course__title')
    inlines = [RecommendationReasonInline]

@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    list_display = ('recommendation', 'student', 'feedback_type', 'created_at')
    list_filter = ('feedback_type', 'created_at')
    search_fields = ('student__user__email', 'comments')
