from django.contrib import admin
from .models import StudentProfile, StudentInterest, StudentCareerGoal, StudentSkill, StudentSkillHistory

class StudentSkillInline(admin.TabularInline):
    model = StudentSkill
    extra = 1

class StudentInterestInline(admin.TabularInline):
    model = StudentInterest
    extra = 1

class StudentCareerGoalInline(admin.TabularInline):
    model = StudentCareerGoal
    extra = 1

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'branch', 'regulation', 'current_semester', 'cgpa', 'onboarding_completed')
    list_filter = ('college', 'branch', 'regulation', 'current_semester', 'onboarding_completed')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    inlines = [StudentSkillInline, StudentInterestInline, StudentCareerGoalInline]

@admin.register(StudentSkillHistory)
class StudentSkillHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'old_proficiency', 'new_proficiency', 'change_source', 'created_at')
    list_filter = ('change_source', 'created_at')
    search_fields = ('student__user__email', 'skill__name')
