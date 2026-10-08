from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentSkill
from apps.skills.models import SkillCategory, Skill
from apps.assessments.models import (
    Assessment, AssessmentQuestion, AssessmentOption,
    AssessmentAttempt, StudentAnswer, AssessmentResult
)

User = get_user_model()

class AssessmentVerificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="ass_student@example.com", username="astudent", password="Password123!")
        self.profile = StudentProfile.objects.create(user=self.user, current_semester=4, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.category = SkillCategory.objects.create(name="Programming")
        self.skill = Skill.objects.create(name="Python", code="PY", category=self.category)

        self.assessment = Assessment.objects.create(
            title="Python Test",
            assessment_type=Assessment.Type.SKILL_LEVEL,
            duration_minutes=20,
            total_marks=10.0,
            passing_marks=7.0
        )

        self.q1 = AssessmentQuestion.objects.create(
            assessment=self.assessment,
            skill=self.skill,
            question_text="Q1 text",
            marks=5.0,
            question_order=1
        )
        self.opt1_corr = AssessmentOption.objects.create(question=self.q1, option_text="Correct", is_correct=True, option_order=1)
        self.opt1_wrong = AssessmentOption.objects.create(question=self.q1, option_text="Wrong", is_correct=False, option_order=2)

        self.q2 = AssessmentQuestion.objects.create(
            assessment=self.assessment,
            skill=self.skill,
            question_text="Q2 text",
            marks=5.0,
            question_order=2
        )
        self.opt2_corr = AssessmentOption.objects.create(question=self.q2, option_text="Correct", is_correct=True, option_order=1)

    def test_list_assessments(self):
        url = reverse('assessment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)

    def test_full_assessment_workflow_and_skill_upgrade(self):
        # 1. Start assessment
        start_url = reverse('assessment-start', kwargs={'pk': str(self.assessment.id)})
        start_resp = self.client.post(start_url)
        self.assertEqual(start_resp.status_code, status.HTTP_200_OK)
        attempt_id = start_resp.data['data']['attempt_id']

        # 2. Record answers
        ans_url = reverse('assessment-answer', kwargs={'attempt_id': str(attempt_id)})
        self.client.post(ans_url, {'question_id': str(self.q1.id), 'option_id': str(self.opt1_corr.id)}, format='json')
        self.client.post(ans_url, {'question_id': str(self.q2.id), 'option_id': str(self.opt2_corr.id)}, format='json')

        # 3. Submit assessment
        sub_url = reverse('assessment-submit', kwargs={'attempt_id': str(attempt_id)})
        sub_resp = self.client.post(sub_url)
        self.assertEqual(sub_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(float(sub_resp.data['data']['percentage']), 100.0)

        # 4. Verify StudentSkill proficiency upgraded to 5
        student_skill = StudentSkill.objects.get(student=self.profile, skill=self.skill)
        self.assertEqual(student_skill.proficiency, 5)
        self.assertEqual(student_skill.source, StudentSkill.SourceChoice.ASSESSMENT_RESULT)
