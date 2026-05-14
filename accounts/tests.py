from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

# Create your tests here.


# Tests related to user registration
class AccountRegistrationTests(TestCase):

    # Test that the registration page loads successfully
    def test_register_page_loads(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    # Test that a new user and profile can be created successfully
    def test_user_can_register(self):
        response = self.client.post(reverse("accounts:register"), {
            "first_name": "Shan",
            "last_name": "Rath",
            "username": "shan",
            "password": "testpassword123",
            "email": "shan@example.com",
            "department": "cs",
        })

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username="shan")
        profile = UserProfile.objects.get(user=user)

        self.assertEqual(user.email, "shan@example.com")
        self.assertEqual(user.first_name, "Shan")
        self.assertEqual(user.last_name, "Rath")
        self.assertEqual(profile.department, "cs")
        self.assertEqual(profile.role, "academic")
        self.assertFalse(profile.is_approved)

    # Test that duplicate usernames are rejected
    def test_duplicate_username_shows_error(self):
        User.objects.create_user(
            username="shan",
            email="old@example.com",
            password="testpassword123"
        )

        response = self.client.post(reverse("accounts:register"), {
            "first_name": "New",
            "last_name": "User",
            "username": "shan",
            "password": "testpassword123",
            "email": "new@example.com",
            "department": "cs",
        })

        self.assertContains(response, "Username shan already exists.")

    # Test that duplicate emails are rejected
    def test_duplicate_email_shows_error(self):
        User.objects.create_user(
            username="olduser",
            email="shan@example.com",
            password="testpassword123"
        )

        response = self.client.post(reverse("accounts:register"), {
            "first_name": "Shan",
            "last_name": "Rathnayake",
            "username": "newuser",
            "password": "testpassword123",
            "email": "shan@example.com",
            "department": "cs",
        })

        self.assertContains(response, "Email shan@example.com already exists.")


# Tests related to user login
class AccountLoginTests(TestCase):

    # Create a default user before each login test
    def setUp(self):
        self.user = User.objects.create_user(
            username="shan",
            password="testpassword123",
            email="shan@example.com"
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            department="cs",
            role="academic",
            is_approved=False
        )

    # Test that the login page loads successfully
    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    # Test that invalid credentials show an error
    def test_invalid_login_shows_error(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "shan",
            "password": "wrongpassword",
        })

        self.assertContains(response, "Invalid username or password.")

    # Test that users cannot log in until approved
    def test_unapproved_user_cannot_login(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "shan",
            "password": "testpassword123",
        })

        self.assertContains(
            response,
            "Your account is awaiting admin approval."
        )

    # Test that approved academic users can log in
    def test_approved_academic_can_login(self):
        self.profile.is_approved = True
        self.profile.save()

        response = self.client.post(reverse("accounts:login"), {
            "username": "shan",
            "password": "testpassword123",
        })

        self.assertContains(
            response,
            "Login successful. You can now submit requests."
        )

    # Test that approved CMS IT users are redirected to admin
    def test_cms_it_redirects_to_admin(self):
        self.profile.is_approved = True
        self.profile.role = "cms_it"
        self.profile.save()

        response = self.client.post(reverse("accounts:login"), {
            "username": "shan",
            "password": "testpassword123",
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/", response.url)