from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SkillCategoryViewSet, SkillViewSet,
    SkillPrerequisiteViewSet, InterestViewSet
)

router = DefaultRouter()
router.register(r'skill-categories', SkillCategoryViewSet, basename='skill-category')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'skill-prerequisites', SkillPrerequisiteViewSet, basename='skill-prerequisite')
router.register(r'interests', InterestViewSet, basename='interest')

urlpatterns = [
    path('', include(router.urls)),
]
