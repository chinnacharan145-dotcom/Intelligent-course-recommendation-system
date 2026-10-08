from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentCareerGoal, StudentSkill
from apps.skills.models import SkillCategory, Skill
from apps.careers.models import Career, CareerSkill
from apps.courses.models import CourseProvider, CourseCategory, Course, CourseSkill
from apps.recommendations.models import Recommendation, RecommendationFeedback

User = get_user_model()

class RecommendationEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="teststudent@example.com", username="teststudent", password="Password123!")
        self.profile = StudentProfile.objects.create(user=self.user, current_semester=4, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.skill_cat = SkillCategory.objects.create(name="AI & ML")
        self.python_skill = Skill.objects.create(name="Python", code="PY", category=self.skill_cat)
        self.ml_skill = Skill.objects.create(name="Machine Learning", code="ML", category=self.skill_cat)

        # Student has Python level 2
        StudentSkill.objects.create(student=self.profile, skill=self.python_skill, proficiency=2)

        # Career Goal: AI Engineer needing ML (level 4) and Python (level 4)
        self.career = Career.objects.create(name="AI Engineer", slug="ai-engineer")
        StudentCareerGoal.objects.create(student=self.profile, career=self.career, is_primary=True)
        CareerSkill.objects.create(career=self.career, skill=self.python_skill, required_level=4, importance=5)
        CareerSkill.objects.create(career=self.career, skill=self.ml_skill, required_level=4, importance=5)

        # Course that teaches ML & Python
        self.provider = CourseProvider.objects.create(name="Coursera")
        self.course_cat = CourseCategory.objects.create(name="AI")
        self.course = Course.objects.create(
            title="Machine Learning Specialization",
            provider=self.provider,
            category=self.course_cat,
            difficulty=Course.Difficulty.INTERMEDIATE,
            rating=4.9
        )
        CourseSkill.objects.create(course=self.course, skill=self.ml_skill, level=4)
        CourseSkill.objects.create(course=self.course, skill=self.python_skill, level=4)

    def test_generate_and_list_recommendations(self):
        url = reverse('recommendation-list')
        response = self.client.get(url, {'refresh': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertGreater(len(response.data['data']), 0)
        
        first_rec = response.data['data'][0]
        self.assertEqual(first_rec['course']['title'], "Machine Learning Specialization")
        self.assertGreater(float(first_rec['match_score']), 50.0)

    def test_recommendation_explanation(self):
        url = reverse('recommendation-list')
        self.client.get(url, {'refresh': 'true'})
        rec = Recommendation.objects.get(student=self.profile)

        exp_url = reverse('recommendation-explanation', kwargs={'pk': str(rec.id)})
        exp_resp = self.client.get(exp_url)
        self.assertEqual(exp_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(exp_resp.data['success'])
        self.assertIn("course_title", exp_resp.data['data'])

    def test_recommendation_feedback(self):
        url = reverse('recommendation-list')
        self.client.get(url, {'refresh': 'true'})
        rec = Recommendation.objects.get(student=self.profile)

        fb_url = reverse('recommendation-feedback', kwargs={'pk': str(rec.id)})
        fb_resp = self.client.post(fb_url, {'feedback_type': 'INTERESTED', 'comments': 'Great course!'}, format='json')
        self.assertEqual(fb_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(RecommendationFeedback.objects.filter(recommendation=rec).count(), 1)
