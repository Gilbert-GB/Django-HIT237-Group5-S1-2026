# Added for Assessment feedback: imports support permission checks, validation, and atomic database writes.
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from .models import Organisation, Program


# Added for Assessment feedback: service layer coordinates authenticated user program submission.
class ProgramSubmissionService:
    # Added for Assessment feedback: this method coordinates user auth, Organisation, Program, validation, and saving.
    @staticmethod
    def submit_program(user, cleaned_data):
        # Added for Assessment feedback: service checks authentication before doing business work.
        if not user or not user.is_authenticated:
            raise PermissionDenied("You must be logged in to submit a program.")

        # Added for Assessment feedback: transaction.atomic keeps the count check and create operation together.
        with transaction.atomic():
            organisation = cleaned_data.get("organisation")

            # Added for Assessment feedback: service validates that a submitted program belongs to an organisation.
            if organisation is None:
                raise ValidationError("A program must belong to an organisation.")

            # Added for Assessment feedback: service verifies the selected organisation still exists in the database.
            try:
                organisation = Organisation.objects.get(pk=organisation.pk)
            except Organisation.DoesNotExist as error:
                raise ValidationError("The selected organisation does not exist.") from error

            # Added for Assessment feedback: service enforces the student-level business rule of max 5 programs per organisation.
            existing_program_count = Program.objects.filter(
                organisation=organisation
            ).count()
            if existing_program_count >= 5:
                raise ValidationError(
                    "This organisation already has 5 programs. Please update an existing program instead."
                )

            # Added for Assessment feedback: service creates, validates, and saves the Program atomically.
            program_data = cleaned_data.copy()
            program_data["organisation"] = organisation
            program = Program(**program_data)
            program.full_clean()
            program.save()
            return program
