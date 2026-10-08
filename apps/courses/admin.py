from django.contrib import admin
from .models import CourseProvider, CourseCategory, Course, CourseSkill, CoursePrerequisite

@admin.register(CourseProvider)
class CourseProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active')
    list_filter = ('is_active',)

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

class CourseSkillInline(admin.TabularInline):
    model = CourseSkill
    extra = 1

class CoursePrerequisiteInline(admin.TabularInline):
    model = CoursePrerequisite
    fk_name = 'course'
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'category', 'difficulty', 'duration_hours', 'is_free', 'rating', 'is_active')
    list_filter = ('provider', 'category', 'difficulty', 'is_free', 'is_active')
    search_fields = ('title', 'description')
    inlines = [CourseSkillInline, CoursePrerequisiteInline]
