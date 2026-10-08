from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentSkill
from apps.courses.models import CourseProvider, CourseCategory, Course, CourseSkill
from apps.skills.models import SkillCategory, Skill
from apps.learning.models import StudentCourse, LearningActivity

User = get_user_model()

class LearningProgressTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="learner@example.com", username="learner", password="Password123!")
        self.profile = StudentProfile.objects.create(user=self.user, current_semester=3, onboarding_completed=True)
        self.client.force_authenticate(user=self.user)

        self.provider = CourseProvider.objects.create(name="NPTEL")
        self.course_cat = CourseCategory.objects.create(name="Computer Science")
        self.skill_cat = SkillCategory.objects.create(name="Core")
        self.skill = Skill.objects.create(name="Algorithms", code="ALG", category=self.skill_cat)

        self.course = Course.objects.create(
            title="Algorithms Course",
            provider=self.provider,
            category=self.course_cat,
            difficulty=Course.Difficulty.BEGINNER,
            rating=4.8
        )

        CourseSkill.objects.create(course=self.course, skill=self.skill, level=4)

    def test_start_and_update_course_progress(self):
        start_url = reverse('course-start', kwargs={'course_id': str(self.course.id)})
        start_resp = self.client.post(start_url)
        self.assertEqual(start_resp.status_code, status.HTTP_200_OK)
        student_course_id = start_resp.data['data']['id']

        update_url = reverse('student-course-update', kwargs={'pk': student_course_id})
        up_resp = self.client.patch(update_url, {'progress': 50.0}, format='json')
        self.assertEqual(up_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(float(up_resp.data['data']['progress']), 50.0)

    def test_complete_course_and_skill_reward(self):
        comp_url = reverse('course-complete', kwargs={'course_id': str(self.course.id)})
        comp_resp = self.client.post(comp_url)
        self.assertEqual(comp_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(comp_resp.data['data']['status'], 'COMPLETED')

        # Check skill awarded
        student_skill = StudentSkill.objects.get(student=self.profile, skill=self.skill)
        self.assertEqual(student_skill.proficiency, 4)
        self.assertEqual(student_skill.source, StudentSkill.SourceChoice.COURSE_COMPLETION)

    def test_student_progress_summary(self):
        start_url = reverse('course-start', kwargs={'course_id': str(self.course.id)})
        self.client.post(start_url)

        prog_url = reverse('student-progress')
        prog_resp = self.client.get(prog_url)
        self.assertEqual(prog_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(prog_resp.data['data']['in_progress_count'], 1)
