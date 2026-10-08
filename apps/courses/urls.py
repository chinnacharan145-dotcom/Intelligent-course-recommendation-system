from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseProviderViewSet, CourseCategoryViewSet,
    CourseViewSet, CourseSkillViewSet, CoursePrerequisiteViewSet
)

router = DefaultRouter()
router.register(r'providers', CourseProviderViewSet, basename='provider')
router.register(r'course-categories', CourseCategoryViewSet, basename='course-category')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'course-skills', CourseSkillViewSet, basename='course-skill')
router.register(r'course-prerequisites', CoursePrerequisiteViewSet, basename='course-prerequisite')

urlpatterns = [
    path('', include(router.urls)),
]
