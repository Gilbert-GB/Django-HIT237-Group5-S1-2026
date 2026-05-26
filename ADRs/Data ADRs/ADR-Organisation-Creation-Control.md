# ADR: Control Organisation Creation Through Django Admin

Status: Accepted
Date created: 2026-05-26
Last updated: 2026-05-26

## Context
The application stores organisations that provide youth justice diversion and support programs. These organisation records are important directory data because many programs can be linked to one organisation.

If any newly registered user could create organisations directly from the public website, the directory could quickly contain duplicate, incorrect, or fake organisation records. The current project does not include an organisation approval workflow or an `OrganisationMembership` model.

## Decision
Only staff/admin users create and manage `Organisation` records through Django admin.

Normal logged-in users can submit programs through the live program creation form, but they must select an existing organisation. Program creation is handled through `ProgramSubmissionService`, while organisation creation remains controlled by admin users.

## Rationale
This keeps the data model simple and protects organisation data quality. Organisation records are more stable than program submissions, so it is reasonable for staff/admin users to maintain them.

This approach also avoids over-engineering. A full public organisation registration flow would require extra validation, approval states, duplicate checking, and possibly an `OrganisationMembership` model. That is outside the current student-project scope.

## Consequences
The directory is less likely to contain fake or duplicate organisations. Logged-in users can still contribute by adding programs for existing organisations.

The trade-off is that a new organisation must be added by an admin before users can submit programs for it. A future version could add an organisation request/approval workflow or organisation membership permissions.

## Evidence in current implementation
- `Organisation` is registered in `youthjustice_app/admin.py`.
- `ProgramForm` includes an `organisation` dropdown for selecting an existing organisation.
- `ProgramSubmissionService` creates programs for existing organisations only.
- There is no public organisation creation view or organisation membership model.