from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentCareerGoal, StudentSkill
from apps.skills.models import SkillCategory, Skill
from apps.careers.models import Career, CareerSkill
from apps.roadmap.models import Roadmap, RoadmapNode

User = get_user_model()

class RoadmapEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="roadmap_student@example.com", username="rmstudent", password="Password123!")
        self.profile = StudentProfile.objects.create(user=self.user, current_semester=4, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.category = SkillCategory.objects.create(name="AI & ML")
        self.python = Skill.objects.create(name="Python", code="PY", category=self.category)
        self.ml = Skill.objects.create(name="Machine Learning", code="ML", category=self.category)

        self.career = Career.objects.create(name="AI Engineer", slug="ai-engineer")
        StudentCareerGoal.objects.create(student=self.profile, career=self.career, is_primary=True)

        CareerSkill.objects.create(career=self.career, skill=self.python, required_level=4, importance=5)
        CareerSkill.objects.create(career=self.career, skill=self.ml, required_level=4, importance=5)

    def test_generate_and_retrieve_roadmap(self):
        url = reverse('roadmap-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']['nodes']), 2)

    def test_complete_roadmap_node(self):
        url = reverse('roadmap-detail')
        self.client.get(url)
        roadmap = Roadmap.objects.get(student=self.profile)
        first_node = roadmap.nodes.first()

        complete_url = reverse('roadmap-node-complete', kwargs={'pk': str(first_node.id)})
        comp_resp = self.client.post(complete_url)
        self.assertEqual(comp_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(comp_resp.data['data']['status'], 'COMPLETED')
        
        roadmap.refresh_from_db()
        self.assertEqual(float(roadmap.overall_progress), 50.0)

    def test_next_best_action(self):
        url = reverse('roadmap-detail')
        self.client.get(url)

        nba_url = reverse('roadmap-next-best-action')
        nba_resp = self.client.get(nba_url)
        self.assertEqual(nba_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(nba_resp.data['data']['action_type'], 'SKILL_ACQUISITION')
