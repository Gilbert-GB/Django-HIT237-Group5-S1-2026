from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from .models import Organisation, Program


# Service layer validates authenticated program submission.
class ProgramSubmissionService:
    # This method matches ProgramCreateView and accepts ProgramForm cleaned_data.
    @staticmethod
    def submit_program(user, cleaned_data):
        # Anonymous users cannot submit programs through the service.
        if not user or not user.is_authenticated:
            raise PermissionDenied("You must be logged in to submit a program.")

        # Service layer ensures the limit check and program save are atomic.
        with transaction.atomic():
            organisation = cleaned_data.get("organisation")

            # Every submitted program must belong to an existing organisation.
            if organisation is None:
                raise ValidationError("A program must belong to an organisation.")

            # Service layer re-fetches the organisation so the service verifies it still exists.
            try:
                organisation = Organisation.objects.get(pk=organisation.pk)
            except Organisation.DoesNotExist as error:
                raise ValidationError("The selected organisation does not exist.") from error

            # Service layer enforces the business rule that one organisation can have max 5 programs.
            existing_program_count = Program.objects.filter(
                organisation=organisation
            ).count()
            if existing_program_count >= 5:
                raise ValidationError(
                    "This organisation already has 5 programs. Please update an existing program instead."
                )

            # Service layer creates, validates, saves, and returns the Program from the service.
            program = Program(**cleaned_data)
            program.full_clean()
            program.save()
            return program
