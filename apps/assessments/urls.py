from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentViewSet, StartAssessmentView, RecordAnswerView,
    SubmitAssessmentView, AssessmentResultView, StudentAssessmentHistoryView
)

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')

urlpatterns = [
    path('assessments/<uuid:pk>/start/', StartAssessmentView.as_view(), name='assessment-start'),
    path('assessment-attempts/<uuid:attempt_id>/answer/', RecordAnswerView.as_view(), name='assessment-answer'),
    path('assessment-attempts/<uuid:attempt_id>/submit/', SubmitAssessmentView.as_view(), name='assessment-submit'),
    path('assessment-attempts/<uuid:attempt_id>/result/', AssessmentResultView.as_view(), name='assessment-result'),
    path('students/me/assessment-history/', StudentAssessmentHistoryView.as_view(), name='student-assessment-history'),
    path('', include(router.urls)),
]
