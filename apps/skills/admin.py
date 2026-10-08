from django.contrib import admin
from .models import SkillCategory, Skill, SkillPrerequisite, Interest

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(SkillPrerequisite)
class SkillPrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('skill', 'prerequisite_skill', 'minimum_level', 'is_mandatory')
    list_filter = ('is_mandatory',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    search_fields = ('name', 'category')
