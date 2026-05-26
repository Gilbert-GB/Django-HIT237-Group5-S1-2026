# ADR: Testing Strategy for Models, Services, Views, and Permission Boundaries

Status: Accepted  
Date created: 2026-05-26  
Last updated: 2026-05-26  

## Context
The assignment requires a meaningful test suite that demonstrates architectural thinking as well as working code. This project now includes model validation rules, manager queries, a transactional service layer for program submission, view-level behavior, and login protection for management pages. A testing strategy is needed so the team can justify what is covered, what is not covered, and why.

## Alternatives
1. Manual testing only
This was not chosen because it is hard to repeat consistently and gives weak evidence for marking. It also makes it easier to miss model validation and permission edge cases.

2. Only testing views
This was not chosen because view tests alone do not prove model validation rules or service-layer business rules. Important logic such as the 5-program organisation limit belongs below the view layer and should be tested directly.

3. Django TestCase coverage for models, services, views, and permission boundaries
This was chosen because it gives balanced coverage without over-engineering. It is suitable for a student project and clearly shows that business rules are checked in the right layers.

## Decision
Use Django `TestCase` tests in `youthjustice_app/tests.py` to cover four areas:

- models: direct validation rules on `Program` and `CrimeData`
- services: `ProgramSubmissionService` authentication, organisation checks, business rules, and save behavior
- views: dashboard API contract and live program creation behavior
- permission boundaries: redirects for anonymous users on protected management pages

The suite remains intentionally compact. It focuses on meaningful business and architectural behavior instead of trying to test every template detail.

## Code reference
- `youthjustice_app/tests.py`
This file contains the test cases for managers, model validation, services, views, and permission boundaries.

- `youthjustice_app/models.py`
This file defines the validation rules that the model tests and service tests exercise, such as age ranges, featured/available rules, and valid crime months.

- `youthjustice_app/managers.py`
This file contains reusable query logic tested through manager-level tests such as `Program.objects.available()`, `Program.objects.search()`, and `CrimeData.objects.total_by_region()`.

- `youthjustice_app/services.py`
This file contains `ProgramSubmissionService`, which is tested directly for authentication, organisation validation, the 5-program limit, and atomic save behavior.

- `youthjustice_app/views.py`
This file contains the protected CRUD views and dashboard API endpoint covered by login-boundary tests and view-level response tests.

## Consequences
Positive:
- Better evidence for marking
- Safer refactoring
- Confirms model validation, service-layer rules, views, and permission boundaries

Negative:
- Does not test full browser UI styling
- Does not test JavaScript chart rendering directly
- Does not fully test large CSV import datasets