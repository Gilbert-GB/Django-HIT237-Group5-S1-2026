from django.core.exceptions import PermissionDenied
from django.db import transaction

from .models import Organisation, Program


# Service layer coordinates Organisation and Program creation atomically.
class ProgramSubmissionService:
    # this method coordinates user auth, organisation lookup, validation, and saving.
    @staticmethod
    def submit_program_for_organisation(user, organisation_id, program_data):
        # Service checks authentication before doing business work.
        if not user or not user.is_authenticated:
            raise PermissionDenied("You must be logged in to submit a program.")

        # Service checks for staff-only permission.
        if not user.is_staff:
            raise PermissionDenied("Only staff users can submit programs.")

        # Service uses transaction.atomic to ensure data consistency.
        with transaction.atomic():
            organisation = Organisation.objects.get(pk=organisation_id)
            program = Program(organisation=organisation, **program_data)
            program.full_clean()
            program.save()
            return program
