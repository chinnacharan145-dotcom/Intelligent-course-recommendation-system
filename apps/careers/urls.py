from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerViewSet, CareerSkillViewSet

router = DefaultRouter()
router.register(r'careers', CareerViewSet, basename='career')
router.register(r'career-skills', CareerSkillViewSet, basename='career-skill')

urlpatterns = [
    path('', include(router.urls)),
]
