from django.urls import path
from .views import AIRecommendationExplanationView

urlpatterns = [
    path('ai/explain-recommendation/<uuid:rec_id>/', AIRecommendationExplanationView.as_view(), name='ai-explain-recommendation'),
]
