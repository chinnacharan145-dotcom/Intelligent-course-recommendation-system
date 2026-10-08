from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentSkill, StudentInterest, StudentCareerGoal
from apps.skills.models import Skill, SkillCategory, Interest
from apps.careers.models import Career, CareerSkill, CareerReadinessSnapshot, SkillGapSnapshot
from apps.academics.models import University, College, Branch, Regulation

User = get_user_model()

class StudentProfileAndReadinessTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="readiness_student@example.com",
            username="rstudent",
            password="Password123!"
        )
        self.profile = StudentProfile.objects.create(user=self.user, current_semester=4, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.category = SkillCategory.objects.create(name="Programming")
        self.python = Skill.objects.create(name="Python", category=self.category)
        self.dsa = Skill.objects.create(name="Data Structures", category=self.category)
        
        self.career = Career.objects.create(name="Software Engineer", slug="software-engineer")
        StudentCareerGoal.objects.create(student=self.profile, career=self.career, is_primary=True)

        # Career requires Python (lvl 4, weight 5, req True -> weight = 10) & DSA (lvl 4, weight 5, req True -> weight = 10)
        # Total weight = 20
        CareerSkill.objects.create(career=self.career, skill=self.python, required_level=4, importance=5, required=True)
        CareerSkill.objects.create(career=self.career, skill=self.dsa, required_level=4, importance=5, required=True)

        # Student has Python at level 4 (earned weight = 10 * (4/4) = 10)
        # Student has no DSA (earned weight = 0)
        # Expected readiness = (10 / 20) * 100 = 50.0%
        StudentSkill.objects.create(student=self.profile, skill=self.python, proficiency=4)

    def test_career_readiness_calculation(self):
        url = reverse('student-career-readiness')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['readiness_percentage'], 50.0)
        self.assertEqual(CareerReadinessSnapshot.objects.filter(student=self.profile).count(), 1)

    def test_skill_gaps_calculation(self):
        url = reverse('student-skill-gaps')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['gaps']), 1)
        self.assertEqual(response.data['data']['gaps'][0]['skill_name'], "Data Structures")
        self.assertEqual(response.data['data']['gaps'][0]['gap'], 4)
        self.assertEqual(SkillGapSnapshot.objects.filter(student=self.profile).count(), 1)
