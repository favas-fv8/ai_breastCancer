from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class AuthApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass12345")
        self.client = APIClient()

    def test_login_success(self):
        resp = self.client.post(
            "/api/auth/login/",
            {"username": "tester", "password": "testpass12345"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.data)

    def test_login_failure(self):
        resp = self.client.post(
            "/api/auth/login/",
            {"username": "tester", "password": "wrong"},
            format="json",
        )
        self.assertEqual(resp.status_code, 401)

    def test_profile_requires_auth(self):
        resp = self.client.get("/api/auth/profile/")
        self.assertEqual(resp.status_code, 401)

    def test_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/auth/profile/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["username"], "tester")

    def test_change_password_flow(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            "/api/auth/password/change/",
            {
                "old_password": "testpass12345",
                "new_password": "newpass12345",
                "confirm_password": "newpass12345",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass12345"))
