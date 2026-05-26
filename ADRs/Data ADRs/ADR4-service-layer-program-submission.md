# ADR-004: Add Service Layer for Program Submission Workflow

Status: Accepted
Date created: 2026-05-26
Last updated: 2026-05-26

## Context
The project already has `youthjustice_app/dashboard_service.py`, which works as a read-only dashboard/query service. The service layer described in class is also useful for user actions that coordinate several parts of the system at once.

Submitting a program is one of those workflows because it involves the authenticated user, an organisation, a program, validation, a program-count business rule, and a database write.

## Decision
Add `youthjustice_app/services.py` with `ProgramSubmissionService`.

`ProgramSubmissionService.submit_program()` allows any authenticated user to submit a program, blocks anonymous users, checks that the selected organisation exists, prevents one organisation from having more than 5 programs, validates the program with `full_clean()`, and saves it inside `transaction.atomic()`.

## Rationale
This workflow should not live fully inside `views.py` because the view should mainly handle HTTP form submission and response handling. It should not live only inside `Program`, because `Program` should not be responsible for checking the current user or counting all programs for an organisation. It should not live only inside `Organisation`, because the workflow creates and validates a separate `Program`.

The service matches the class definition of a service layer because it coordinates user authentication, `Organisation`, `Program`, validation, the 5-program limit, and `transaction.atomic()` for one user action.

## Consequences
The create-program workflow now has a clear transactional business service while keeping the dashboard unchanged. Anonymous users are blocked by `LoginRequiredMixin` before reaching the create view and also by the service if it is called directly. The 5-program limit is enforced in the service instead of only in a form or template.

## Evidence in current implementation
- `youthjustice_app/services.py` contains `ProgramSubmissionService`.
- `ProgramSubmissionService.submit_program()` coordinates authentication, organisation lookup, program creation, validation, the 5-program limit, and `transaction.atomic()`.
- `ProgramCreateView.form_valid()` in `youthjustice_app/views.py` uses `ProgramSubmissionService`.
- `youthjustice_app/tests.py` tests authenticated submission, anonymous blocking, invalid age validation, the 5-program limit, and live view integration.
- `youthjustice_app/dashboard_service.py` remains unchanged as a read-only dashboard/query service.