from django.contrib import admin
from .models import University, College, Branch, Regulation, AcademicYear, Semester, Subject, BranchSubject

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'website', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'university', 'location', 'is_active')
    search_fields = ('name', 'code', 'location')
    list_filter = ('university', 'is_active')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('code', 'name')

@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'start_year', 'end_year', 'is_active')
    list_filter = ('university', 'is_active')

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'description')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)

@admin.register(BranchSubject)
class BranchSubjectAdmin(admin.ModelAdmin):
    list_display = ('branch', 'regulation', 'semester', 'subject', 'is_elective')
    list_filter = ('branch', 'regulation', 'semester', 'is_elective')
