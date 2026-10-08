from django.urls import path
from .views import (
    RoadmapView, RoadmapRecalculateView,
    RoadmapNodeCompleteView, NextBestActionView
)

urlpatterns = [
    path('roadmap/', RoadmapView.as_view(), name='roadmap-detail'),
    path('roadmap/recalculate/', RoadmapRecalculateView.as_view(), name='roadmap-recalculate'),
    path('roadmap/nodes/<uuid:pk>/complete/', RoadmapNodeCompleteView.as_view(), name='roadmap-node-complete'),
    path('roadmap/next-best-action/', NextBestActionView.as_view(), name='roadmap-next-best-action'),
]
