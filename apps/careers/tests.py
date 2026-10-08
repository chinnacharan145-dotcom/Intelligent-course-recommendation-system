from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.careers.models import Career, CareerSkill
from apps.skills.models import Skill

class CareerIntelligenceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.career = Career.objects.create(
            name="AI Engineer",
            slug="ai-engineer",
            industry="Artificial Intelligence"
        )
        self.skill = Skill.objects.create(name="Python", code="PY")
        self.career_skill = CareerSkill.objects.create(
            career=self.career,
            skill=self.skill,
            required_level=4,
            importance=5,
            required=True
        )

    def test_list_careers(self):
        url = reverse('career-list')
        response = self.client.get(url, {'search': 'AI'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "AI Engineer")

    def test_career_detail_with_skills(self):
        url = reverse('career-detail', kwargs={'pk': str(self.career.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['required_skills']), 1)
        self.assertEqual(response.data['required_skills'][0]['skill_name'], "Python")

    def test_career_skills_list(self):
        url = reverse('career-skill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
