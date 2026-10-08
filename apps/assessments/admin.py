from django.contrib import admin
from .models import (
    Assessment, AssessmentQuestion, AssessmentOption,
    AssessmentAttempt, StudentAnswer, AssessmentResult, AssessmentSkillResult
)

class AssessmentOptionInline(admin.TabularInline):
    model = AssessmentOption
    extra = 4

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'assessment', 'skill', 'marks', 'difficulty', 'question_order')
    list_filter = ('assessment', 'skill', 'difficulty')
    inlines = [AssessmentOptionInline]

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'assessment_type', 'duration_minutes', 'total_marks', 'passing_marks', 'is_active')
    list_filter = ('assessment_type', 'is_active')
    search_fields = ('title', 'description')

@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment', 'status', 'score', 'percentage', 'started_at', 'submitted_at')
    list_filter = ('status', 'assessment')
    search_fields = ('student__user__email', 'assessment__title')

@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'total_questions', 'correct_answers', 'marks_obtained', 'percentage')

@admin.register(AssessmentSkillResult)
class AssessmentSkillResultAdmin(admin.ModelAdmin):
    list_display = ('assessment_result', 'skill', 'questions_count', 'correct_count', 'percentage', 'skill_score')
