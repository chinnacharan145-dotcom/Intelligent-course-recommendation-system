from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile
from apps.courses.models import CourseProvider, CourseCategory, Course
from apps.recommendations.models import Recommendation, RecommendationReason

User = get_user_model()

class AIAssistantEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="ai_student@example.com", username="aistudent", password="Password123!")
        self.profile = StudentProfile.objects.create(user=self.user, current_semester=4, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.provider = CourseProvider.objects.create(name="Coursera")
        self.category = CourseCategory.objects.create(name="AI & ML")
        self.course = Course.objects.create(
            title="Machine Learning Specialization",
            provider=self.provider,
            category=self.category,
            rating=4.9
        )

        self.recommendation = Recommendation.objects.create(
            student=self.profile,
            course=self.course,
            match_score=88.5
        )
        RecommendationReason.objects.create(
            recommendation=self.recommendation,
            reason_type="SCORE_FACTOR",
            reason_text="✓ Addresses key skill gap in Machine Learning",
            priority=1
        )

    def test_ai_explanation_deterministic_fallback(self):
        url = reverse('ai-explain-recommendation', kwargs={'rec_id': str(self.recommendation.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('explanation_text', response.data['data'])
        self.assertIn('DETERMINISTIC', response.data['data']['source'])
