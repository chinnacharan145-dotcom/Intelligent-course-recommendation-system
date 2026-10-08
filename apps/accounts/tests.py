from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.refresh_url = reverse('auth-token-refresh')
        self.logout_url = reverse('auth-logout')
        self.me_url = reverse('auth-me')

        self.user_data = {
            "email": "student@example.com",
            "username": "studentuser",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password123!",
            "confirm_password": "Password123!"
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(StudentProfile.objects.filter(user__email=self.user_data['email']).exists())

    def test_user_login_success(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data']['tokens'])

    def test_user_login_invalid_password(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            "email": self.user_data['email'],
            "password": "WrongPassword!"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_protected_me_endpoint(self):
        reg_resp = self.client.post(self.register_url, self.user_data, format='json')
        access_token = reg_resp.data['data']['tokens']['access']

        # Without token
        unauth_resp = self.client.get(self.me_url)
        self.assertEqual(unauth_resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # With token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        auth_resp = self.client.get(self.me_url)
        self.assertEqual(auth_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(auth_resp.data['data']['email'], self.user_data['email'])

    def test_token_refresh_and_logout(self):
        reg_resp = self.client.post(self.register_url, self.user_data, format='json')
        refresh_token = reg_resp.data['data']['tokens']['refresh']
        access_token = reg_resp.data['data']['tokens']['access']

        # Refresh
        ref_resp = self.client.post(self.refresh_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(ref_resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', ref_resp.data)

        # Logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_resp = self.client.post(self.logout_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(logout_resp.status_code, status.HTTP_200_OK)
