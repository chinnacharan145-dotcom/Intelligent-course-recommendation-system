from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.skills.models import SkillCategory, Skill, SkillPrerequisite, Interest

class SkillTaxonomyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = SkillCategory.objects.create(name="AI & ML")
        self.python = Skill.objects.create(name="Python", category=self.category, code="PY")
        self.ml = Skill.objects.create(name="Machine Learning", category=self.category, code="ML")
        self.dl = Skill.objects.create(name="Deep Learning", category=self.category, code="DL")

        # Python -> ML -> DL
        SkillPrerequisite.objects.create(skill=self.ml, prerequisite_skill=self.python, minimum_level=3)
        SkillPrerequisite.objects.create(skill=self.dl, prerequisite_skill=self.ml, minimum_level=3)

        self.interest = Interest.objects.create(name="AI Research")

    def test_list_skills_and_search(self):
        url = reverse('skill-list')
        response = self.client.get(url, {'search': 'Machine'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Machine Learning")

    def test_skill_graph_endpoint(self):
        url = reverse('skill-graph', kwargs={'pk': str(self.dl.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        prereqs = response.data['data']['prerequisites_tree']
        self.assertEqual(len(prereqs), 1)
        self.assertEqual(prereqs[0]['skill_name'], "Machine Learning")
        self.assertEqual(len(prereqs[0]['sub_prerequisites']), 1)
        self.assertEqual(prereqs[0]['sub_prerequisites'][0]['skill_name'], "Python")

    def test_skill_categories_and_interests(self):
        cat_url = reverse('skill-category-list')
        cat_resp = self.client.get(cat_url)
        self.assertEqual(cat_resp.status_code, status.HTTP_200_OK)

        int_url = reverse('interest-list')
        int_resp = self.client.get(int_url)
        self.assertEqual(int_resp.status_code, status.HTTP_200_OK)
