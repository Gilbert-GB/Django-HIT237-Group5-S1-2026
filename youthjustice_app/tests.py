from django.test import TestCase
from django.urls import reverse

from .models import CrimeData, Organisation, Program


# ADDED FOR HIT237 FEEDBACK:
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

    # ADDED FOR HIT237 FEEDBACK:
    # Program.objects.available() proves common filtering is kept in the manager.
    def test_program_available_manager_returns_only_available_programs(self):
        available = self.create_program(name="Available Program")
        self.create_program(name="Unavailable Program", is_available=False)

        self.assertEqual(list(Program.objects.available()), [available])

    # ADDED FOR HIT237 FEEDBACK:
    # Program.objects.search() proves manager-based search can be reused by views.
    def test_program_search_manager_finds_available_matching_programs(self):
        matching = self.create_program(name="Darwin Mentoring Circle")
        self.create_program(name="Unavailable Mentoring", is_available=False)

        self.assertEqual(list(Program.objects.search("mentoring")), [matching])

    # ADDED FOR HIT237 FEEDBACK:
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


# ADDED FOR HIT237 FEEDBACK:
# This test proves LoginRequiredMixin protects the program management page.
class CrudAccessTests(TestCase):
    def test_manage_programs_requires_login(self):
        response = self.client.get(reverse("manage_programs"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])
