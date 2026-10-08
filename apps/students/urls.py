from django.urls import path
from .views import (
    StudentProfileMeView, OnboardingView,
    StudentSkillsView, StudentSkillDetailView,
    StudentInterestsView, StudentCareerGoalsView,
    SkillGapsView, CareerReadinessView
)

urlpatterns = [
    path('me/', StudentProfileMeView.as_view(), name='student-me'),
    path('onboarding/', OnboardingView.as_view(), name='student-onboarding'),
    path('me/skills/', StudentSkillsView.as_view(), name='student-skills'),
    path('me/skills/<uuid:pk>/', StudentSkillDetailView.as_view(), name='student-skill-detail'),
    path('me/interests/', StudentInterestsView.as_view(), name='student-interests'),
    path('me/career-goals/', StudentCareerGoalsView.as_view(), name='student-career-goals'),
    path('me/skill-gaps/', SkillGapsView.as_view(), name='student-skill-gaps'),
    path('me/career-readiness/', CareerReadinessView.as_view(), name='student-career-readiness'),
]
