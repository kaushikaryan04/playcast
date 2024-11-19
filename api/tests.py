from django.test import TestCase
from rest_framework.test import APIClient , APITestCase
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework import status


class JwtTesting(APITestCase):
    def setUp(self) :
        self.register_url = "/api/register"
        self.login_url = "/api/login"
        self.protected_url = "/api/listvideos"

        self.client = APIClient()

        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password2": "testpassword123",
        }
    def test_signup_user(self):

        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(User.objects.get(username = self.user_data["username"]).username ,self.user_data["username"] )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_valid_credentials(self):
        # First, register the user
        self.client.post(self.register_url, self.user_data)


        login_data = {"username": self.user_data["username"], "password": self.user_data["password"]}
        response = self.client.post(self.login_url, login_data)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):

        self.client.post(self.register_url, self.user_data)


        login_data = {"username": self.user_data["username"], "password": "wrongpassword"}
        response = self.client.post(self.login_url, login_data)


        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_access_protected_endpoint_with_valid_token(self):

        self.client.post(self.register_url, self.user_data)
        login_data = {"username": self.user_data["username"], "password": self.user_data["password"]}
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data.get("access")


        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


        protected_response = self.client.get(self.protected_url)


        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_with_invalid_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")


        protected_response = self.client.get(self.protected_url)

        self.assertEqual(protected_response.status_code, status.HTTP_401_UNAUTHORIZED)
