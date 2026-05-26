from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import CrimeData, Organisation, Program
from .services import ProgramSubmissionService

# These tests demonstrate the existing custom manager methods in a simple way.
class ManagerTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(
            name="Darwin Youth Support",
            email="support@example.com",
        )

    def create_program(self, **overrides):
        data = {
            "name": "Mentoring Program",
            "organisation": self.organisation,
            "region": "darwin",
            "category": "mentoring",
            "age_min": 12,
            "age_max": 17,
            "is_available": True,
            "is_featured": False,
            "short_description": "Support for young people.",
        }
        data.update(overrides)
        return Program.objects.create(**data)

    # Program.objects.available() proves common filtering is kept in the manager.
    def test_program_available_manager_returns_only_available_programs(self):
        available = self.create_program(name="Available Program")
        self.create_program(name="Unavailable Program", is_available=False)

        self.assertEqual(list(Program.objects.available()), [available])

    # Program.objects.search() proves manager-based search can be reused by views.
    def test_program_search_manager_finds_available_matching_programs(self):
        matching = self.create_program(name="Darwin Mentoring Circle")
        self.create_program(name="Unavailable Mentoring", is_available=False)

        self.assertEqual(list(Program.objects.search("mentoring")), [matching])

    # CrimeData.objects.total_by_region() demonstrates values() plus annotate(Sum()).
    def test_crime_data_total_by_region_aggregation(self):
        CrimeData.objects.create(
            year=2024,
            month=1,
            offence_category="02 Assault",
            offence_type="Common assault",
            alcohol_involvement="No",
            dv_involvement="No",
            region="Darwin",
            count=10,
        )
        CrimeData.objects.create(
            year=2024,
            month=2,
            offence_category="02 Assault",
            offence_type="Common assault",
            alcohol_involvement="No",
            dv_involvement="No",
            region="Darwin",
            count=5,
        )

        totals = list(CrimeData.objects.total_by_region())

        self.assertEqual(totals[0]["region"], "Darwin")
        self.assertEqual(totals[0]["total"], 15)


# This test proves LoginRequiredMixin protects the program management page.
class CrudAccessTests(TestCase):
    def test_manage_programs_requires_login(self):
        response = self.client.get(reverse("manage_programs"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])


# These tests prove the transactional service layer workflow.
class ProgramSubmissionServiceTests(TestCase):
    # Added for Assessment feedback: common setup creates one organisation and valid program data.
    def setUp(self):
        self.organisation = Organisation.objects.create(
            name="Service Test Organisation",
            email="service@example.com",
        )
        self.program_data = {
            "name": "Service Layer Program",
            "organisation": self.organisation,
            "region": "darwin",
            "category": "support",
            "age_min": 12,
            "age_max": 17,
            "is_available": True,
            "is_featured": False,
            "short_description": "Created through the service layer.",
        }

    # Unauthenticated users cannot use the submission service.
    def test_unauthenticated_user_cannot_submit_program(self):
        with self.assertRaises(PermissionDenied):
            ProgramSubmissionService.submit_program(
                user=AnonymousUser(),
                cleaned_data=self.program_data,
            )

    # Any authenticated normal user can submit through the service.
    def test_authenticated_normal_user_can_submit_program(self):
        user = User.objects.create_user(username="regular", password="testpass123")

        program = ProgramSubmissionService.submit_program(
            user=user,
            cleaned_data=self.program_data,
        )

        self.assertEqual(program.organisation, self.organisation)
        self.assertTrue(Program.objects.filter(name="Service Layer Program").exists())

    # Model validation still runs inside the service workflow.
    def test_invalid_age_range_raises_validation_error(self):
        user = User.objects.create_user(username="regular-age", password="testpass123")
        invalid_data = self.program_data.copy()
        invalid_data["age_min"] = 18
        invalid_data["age_max"] = 12

        with self.assertRaises(ValidationError):
            ProgramSubmissionService.submit_program(
                user=user,
                cleaned_data=invalid_data,
            )

        self.assertFalse(Program.objects.filter(name="Service Layer Program").exists())

    # Service blocks a sixth program for the same organisation.
    def test_organisation_with_five_programs_cannot_accept_sixth(self):
        user = User.objects.create_user(username="regular-limit", password="testpass123")
        for number in range(5):
            Program.objects.create(
                name=f"Existing Program {number}",
                organisation=self.organisation,
                region="darwin",
                category="support",
                age_min=12,
                age_max=17,
                is_available=True,
                is_featured=False,
                short_description="Existing program.",
            )

        with self.assertRaises(ValidationError):
            ProgramSubmissionService.submit_program(
                user=user,
                cleaned_data=self.program_data,
            )

        self.assertEqual(Program.objects.filter(organisation=self.organisation).count(), 5)


# These tests prove the live ProgramCreateView uses the service layer.
class ProgramCreateViewServiceTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="testpass123")
        self.organisation = Organisation.objects.create(
            name="Create View Organisation",
            email="create@example.com",
        )

    # Helper returns valid POST data for the ProgramForm.
    def valid_post_data(self, **overrides):
        data = {
            "name": "Create View Program",
            "organisation": self.organisation.pk,
            "region": "darwin",
            "category": "support",
            "age_min": 12,
            "age_max": 17,
            "is_available": "on",
            "short_description": "Created through the live form.",
            "website": "",
        }
        data.update(overrides)
        return data

    # These tests prove the live ProgramCreateView uses the service layer.
    def test_program_create_view_uses_service_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("add_program"), self.valid_post_data())

        self.assertRedirects(response, reverse("manage_programs"))
        self.assertTrue(Program.objects.filter(name="Create View Program").exists())

    # These tests prove the live ProgramCreateView uses the service layer.
    def test_program_create_view_shows_error_when_organisation_has_five_programs(self):
        self.client.force_login(self.user)
        for number in range(5):
            Program.objects.create(
                name=f"Existing Create View Program {number}",
                organisation=self.organisation,
                region="darwin",
                category="support",
                age_min=12,
                age_max=17,
                is_available=True,
                is_featured=False,
                short_description="Existing program.",
            )

        response = self.client.post(reverse("add_program"), self.valid_post_data())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This organisation already has 5 programs")
        self.assertFalse(Program.objects.filter(name="Create View Program").exists())
