from django.contrib import admin
from .models import Career, CareerSkill, CareerReadinessSnapshot, SkillGapSnapshot

class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 1

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'salary_min', 'salary_max', 'is_active')
    list_filter = ('industry', 'is_active')
    search_fields = ('name', 'description')
    inlines = [CareerSkillInline]

@admin.register(CareerReadinessSnapshot)
class CareerReadinessSnapshotAdmin(admin.ModelAdmin):
    list_display = ('student', 'career', 'readiness_score', 'calculated_at')
    list_filter = ('career', 'calculated_at')

@admin.register(SkillGapSnapshot)
class SkillGapSnapshotAdmin(admin.ModelAdmin):
    list_display = ('student', 'career', 'total_gaps_count', 'avg_gap_size', 'calculated_at')
    list_filter = ('career', 'calculated_at')
