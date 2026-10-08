from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.courses.models import CourseProvider, CourseCategory, Course, CourseSkill, CoursePrerequisite
from apps.skills.models import Skill

class CourseEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.provider = CourseProvider.objects.create(name="Coursera", website="https://coursera.org")
        self.category = CourseCategory.objects.create(name="AI & ML")
        self.skill = Skill.objects.create(name="Python", code="PY")

        self.course = Course.objects.create(
            title="Machine Learning Specialization",
            provider=self.provider,
            category=self.category,
            difficulty=Course.Difficulty.INTERMEDIATE,
            duration_hours=40.0,
            rating=4.9,
            is_free=True
        )

        CourseSkill.objects.create(course=self.course, skill=self.skill, level=4)
        CoursePrerequisite.objects.create(course=self.course, required_skill=self.skill, minimum_level=2)

    def test_list_and_filter_courses(self):
        url = reverse('course-list')
        response = self.client.get(url, {'search': 'Machine', 'free': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Machine Learning Specialization")

    def test_course_detail_with_skills_and_prereqs(self):
        url = reverse('course-detail', kwargs={'pk': str(self.course.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['skills']), 1)
        self.assertEqual(response.data['skills'][0]['skill_name'], "Python")
        self.assertEqual(len(response.data['prerequisites']), 1)
        self.assertEqual(response.data['prerequisites'][0]['required_skill_name'], "Python")

    def test_providers_and_categories(self):
        prov_url = reverse('provider-list')
        prov_resp = self.client.get(prov_url)
        self.assertEqual(prov_resp.status_code, status.HTTP_200_OK)

        cat_url = reverse('course-category-list')
        cat_resp = self.client.get(cat_url)
        self.assertEqual(cat_resp.status_code, status.HTTP_200_OK)
