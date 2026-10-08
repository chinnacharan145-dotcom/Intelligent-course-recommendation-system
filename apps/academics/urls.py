from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet, CollegeViewSet, BranchViewSet,
    RegulationViewSet, AcademicYearViewSet, SemesterViewSet,
    SubjectViewSet, BranchSubjectViewSet
)

router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'colleges', CollegeViewSet, basename='college')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'regulations', RegulationViewSet, basename='regulation')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'branch-subjects', BranchSubjectViewSet, basename='branch-subject')

urlpatterns = [
    path('academics/', include(router.urls)),
]
