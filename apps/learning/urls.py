from django.urls import path
from .views import (
    StartCourseView, UpdateCourseProgressView,
    CompleteCourseView, StudentProgressView
)

urlpatterns = [
    path('courses/<uuid:course_id>/start/', StartCourseView.as_view(), name='course-start'),
    path('student-courses/<uuid:pk>/', UpdateCourseProgressView.as_view(), name='student-course-update'),
    path('courses/<uuid:course_id>/complete/', CompleteCourseView.as_view(), name='course-complete'),
    path('students/me/progress/', StudentProgressView.as_view(), name='student-progress'),
]
