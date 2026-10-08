from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.academics.models import University, College, Branch, Regulation, Semester, Subject, BranchSubject

User = get_user_model()

class AcademicHierarchyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.university = University.objects.create(name="JNTU Hyderabad", code="JNTUH")
        self.college = College.objects.create(name="CBIT", code="CBIT", university=self.university)
        self.branch = Branch.objects.create(name="Computer Science", code="CSE")
        self.regulation = Regulation.objects.create(name="R20", university=self.university, start_year=2020)
        self.semester = Semester.objects.create(number=3, name="Semester 3")
        self.subject = Subject.objects.create(code="CS101", name="Data Structures", credits=4.0)
        self.branch_subject = BranchSubject.objects.create(
            branch=self.branch,
            regulation=self.regulation,
            semester=self.semester,
            subject=self.subject,
            is_elective=False
        )

        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="AdminPassword123!"
        )

    def test_get_universities(self):
        url = reverse('university-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['code'], "JNTUH")

    def test_filter_colleges_by_university(self):
        url = reverse('college-list')
        response = self.client.get(url, {'university': str(self.university.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)

    def test_filter_branch_subjects(self):
        url = reverse('branch-subject-list')
        params = {
            'branch': str(self.branch.id),
            'regulation': str(self.regulation.id),
            'semester': str(self.semester.id)
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['subject_details']['code'], "CS101")

    def test_admin_create_university(self):
        url = reverse('university-list')
        data = {"name": "Osmania University", "code": "OU"}

        # Anonymous request blocked
        unauth_resp = self.client.post(url, data, format='json')
        self.assertEqual(unauth_resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Admin request allowed
        self.client.force_authenticate(user=self.admin_user)
        auth_resp = self.client.post(url, data, format='json')
        self.assertEqual(auth_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(University.objects.count(), 2)
