from django.urls import path
from .views import StudentDashboardView, AdminAnalyticsView

urlpatterns = [
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('admin/dashboard/', AdminAnalyticsView.as_view(), name='admin-analytics-dashboard'),
]
