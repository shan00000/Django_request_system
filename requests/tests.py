from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import SoftwareRequest, RequestCycle


class RequestAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="shan",
            password="testpassword123"
        )

        self.other_user = User.objects.create_user(
            username="other",
            password="testpassword123"
        )

        self.active_cycle = RequestCycle.objects.create(
            year=str(timezone.now().year),
            is_active=True,
            opens_at=timezone.now().date(),
            closes_at=timezone.now().date() + timedelta(days=30)
        )

        self.request_obj = SoftwareRequest.objects.create(
            requested_by=self.user,
            application_name="PyCharm",
            application_description="Python IDE",
            application_website="https://example.com",
            purchase_required=False,
            need_virtual_desktop=True,
            alternative_software_has_been_considered=True,
            license_agreement_detail="Test license",
            privacy_considered=True,
            primary_use="Teaching",
            need_installing_on="GR116",
            need_staff_machine=False,
            anything_else="Nothing else",
            start_date=timezone.now().date(),
        )

    # Test dashboard requires login
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("requests:dashboard"))

        self.assertEqual(response.status_code, 302)

    # Test logged-in user can view dashboard
    def test_dashboard_loads_for_logged_in_user(self):
        self.client.login(username="shan", password="testpassword123")

        response = self.client.get(reverse("requests:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "requests/dashboard.html")

    # Test dashboard only shows requests belonging to the logged-in user
    def test_dashboard_only_shows_own_requests(self):
        SoftwareRequest.objects.create(
            requested_by=self.other_user,
            application_name="Other User Software",
            application_description="Should not be visible",
            application_website="https://example.com",
            primary_use="Other",
            need_installing_on="Other room",
            start_date=timezone.now().date(),
        )

        self.client.login(username="shan", password="testpassword123")

        response = self.client.get(reverse("requests:dashboard"))

        self.assertContains(response, "PyCharm")
        self.assertNotContains(response, "Other User Software")

    # Test request detail page loads for owner
    def test_request_detail_loads_for_owner(self):
        self.client.login(username="shan", password="testpassword123")

        response = self.client.get(
            reverse("requests:request_detail", args=[self.request_obj.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PyCharm")

    # Test user cannot view another user's request detail
    def test_user_cannot_view_other_users_request(self):
        other_request = SoftwareRequest.objects.create(
            requested_by=self.other_user,
            application_name="Secret Software",
            application_description="Private",
            application_website="https://example.com",
            primary_use="Private",
            need_installing_on="Private room",
            start_date=timezone.now().date(),
        )

        self.client.login(username="shan", password="testpassword123")

        response = self.client.get(
            reverse("requests:request_detail", args=[other_request.pk])
        )

        self.assertEqual(response.status_code, 404)

    # Test new request can be created when request cycle is active
    def test_user_can_create_request_when_cycle_active(self):
        self.client.login(username="shan", password="testpassword123")

        response = self.client.post(reverse("requests:new_request"), {
            "application_name": "VS Code",
            "application_description": "Code editor",
            "application_website": "https://example.com",
            "purchase_required": "on",
            "need_virtual_desktop": "on",
            "alternative_software_has_been_considered": "on",
            "license_agreement_detail": "License details",
            "privacy_considered": "on",
            "primary_use": "Teaching",
            "need_installing_on": "GR115",
            "need_staff_machine": "on",
            "anything_else": "No extra info",
            "start_date": timezone.now().date(),
        })

        self.assertRedirects(response, reverse("requests:dashboard"))
        self.assertTrue(
            SoftwareRequest.objects.filter(application_name="VS Code").exists()
        )

    # Test new request cannot be created when request cycle is closed
    def test_user_cannot_create_request_when_cycle_closed(self):
        self.active_cycle.is_active = False
        self.active_cycle.save()

        self.client.login(username="shan", password="testpassword123")

        response = self.client.post(reverse("requests:new_request"), {
            "application_name": "Closed Cycle Software",
            "application_description": "Should not save",
            "application_website": "https://example.com",
            "primary_use": "Teaching",
            "need_installing_on": "GR116",
            "start_date": timezone.now().date(),
        })

        self.assertContains(response, "Request period is currently closed.")
        self.assertFalse(
            SoftwareRequest.objects.filter(
                application_name="Closed Cycle Software"
            ).exists()
        )

    # Test submitted current-year request can be edited
    def test_user_can_edit_submitted_current_year_request(self):
        self.client.login(username="shan", password="testpassword123")

        response = self.client.post(
            reverse("requests:edit_request", args=[self.request_obj.pk]),
            {
                "application_name": "Updated PyCharm",
                "application_description": "Updated description",
                "application_website": "https://example.com",
                "license_agreement_detail": "Updated license",
                "primary_use": "Updated use",
                "need_installing_on": "GR117",
                "anything_else": "Updated extra",
                "start_date": timezone.now().date(),
            }
        )

        self.assertRedirects(
            response,
            reverse("requests:request_detail", args=[self.request_obj.pk])
        )

        self.request_obj.refresh_from_db()
        self.assertEqual(self.request_obj.application_name, "Updated PyCharm")

    # Test request cannot be edited after status changes from submitted
    def test_user_cannot_edit_request_after_status_changes(self):
        self.request_obj.status = "in_review"
        self.request_obj.save()

        self.client.login(username="shan", password="testpassword123")

        response = self.client.post(
            reverse("requests:edit_request", args=[self.request_obj.pk]),
            {
                "application_name": "Should Not Update",
                "application_description": "No",
                "application_website": "https://example.com",
                "primary_use": "No",
                "need_installing_on": "No",
                "start_date": timezone.now().date(),
            }
        )

        self.assertRedirects(
            response,
            reverse("requests:request_detail", args=[self.request_obj.pk])
        )

        self.request_obj.refresh_from_db()
        self.assertEqual(self.request_obj.application_name, "PyCharm")

    # Test current-year request cannot be renewed
    def test_current_year_request_cannot_be_renewed(self):
        self.client.login(username="shan", password="testpassword123")

        response = self.client.get(
            reverse("requests:renew_request", args=[self.request_obj.pk])
        )

        self.assertRedirects(
            response,
            reverse("requests:request_detail", args=[self.request_obj.pk])
        )

        self.assertEqual(
            SoftwareRequest.objects.filter(application_name="PyCharm").count(),
            1
        )

    # Test logout redirects user to login page
    def test_logout_redirects_to_login(self):
        self.client.login(username="shan", password="testpassword123")

        response = self.client.get(reverse("requests:logout"))

        self.assertRedirects(response, reverse("accounts:login"))