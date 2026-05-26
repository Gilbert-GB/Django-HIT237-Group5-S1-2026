from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsAuthTests(TestCase):
  
    # The login page should render for users who are not signed in.
    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")


    # Registering should create the user and auto-login through register_view.
    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass12345",
                "password2": "StrongPass12345",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertIn("_auth_user_id", self.client.session)

    # The custom logout view should end the session and redirect to login.
    def test_logout_redirects_to_login(self):
        user = User.objects.create_user(
            username="existinguser",
            password="StrongPass12345",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
