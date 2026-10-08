from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentCareerGoal
from apps.careers.models import Career, CareerSkill
from apps.skills.models import SkillCategory, Skill
from apps.courses.models import CourseProvider, CourseCategory, Course

User = get_user_model()

class AnalyticsDashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Student
        self.student_user = User.objects.create_user(email="dash_student@example.com", username="dstudent", password="Password123!")
        self.student_profile = StudentProfile.objects.create(user=self.student_user, current_semester=4, onboarding_completed=True)

        # Admin
        self.admin_user = User.objects.create_superuser(email="dash_admin@example.com", username="dadmin", password="Password123!")

        # Skill & Career & Course
        self.category = SkillCategory.objects.create(name="AI & ML")
        self.python = Skill.objects.create(name="Python", code="PY", category=self.category)
        self.career = Career.objects.create(name="AI Engineer", slug="ai-engineer")
        StudentCareerGoal.objects.create(student=self.student_profile, career=self.career, is_primary=True)
        CareerSkill.objects.create(career=self.career, skill=self.python, required_level=4, importance=5)

        self.provider = CourseProvider.objects.create(name="Coursera")
        self.course_cat = CourseCategory.objects.create(name="AI")
        self.course = Course.objects.create(title="Python for AI", provider=self.provider, category=self.course_cat, rating=4.9)

    def test_student_dashboard_analytics(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('student-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('profile_completion', response.data['data'])
        self.assertIn('career_readiness', response.data['data'])
        self.assertIn('top_recommendations', response.data['data'])

    def test_admin_analytics_dashboard(self):
        url = reverse('admin-analytics-dashboard')
        
        # Unauthenticated / Student forbidden or unauth
        self.client.force_authenticate(user=self.student_user)
        unauth_resp = self.client.get(url)
        self.assertEqual(unauth_resp.status_code, status.HTTP_403_FORBIDDEN)

        # Admin authorized
        self.client.force_authenticate(user=self.admin_user)
        admin_resp = self.client.get(url)
        self.assertEqual(admin_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_resp.data['data']['total_students'], 1)
        self.assertEqual(admin_resp.data['data']['active_students'], 1)
