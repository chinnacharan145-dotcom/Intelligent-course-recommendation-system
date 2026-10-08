from django.urls import path
from .views import (
    RecommendationListView, GenerateRecommendationView,
    RecommendationDetailView, RecommendationExplanationView,
    RecommendationFeedbackView
)

urlpatterns = [
    path('recommendations/', RecommendationListView.as_view(), name='recommendation-list'),
    path('recommendations/generate/', GenerateRecommendationView.as_view(), name='recommendation-generate'),
    path('recommendations/<uuid:pk>/', RecommendationDetailView.as_view(), name='recommendation-detail'),
    path('recommendations/<uuid:pk>/explanation/', RecommendationExplanationView.as_view(), name='recommendation-explanation'),
    path('recommendations/<uuid:pk>/feedback/', RecommendationFeedbackView.as_view(), name='recommendation-feedback'),
]
