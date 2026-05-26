# ADR: Authentication and CRUD Access Control

<!-- ADDED FOR HIT237 FEEDBACK: new ADR explaining login protection for CRUD pages -->
## Status
Accepted

## Date created
2026-05-26

## Last updated
2026-05-26

## Context
The project includes public pages for browsing and management pages for adding, editing, and deleting programs. Management pages should not be publicly accessible.

## Decision
Use Django authentication and `LoginRequiredMixin` on program CRUD class-based views. This is a simple student-friendly access control approach that uses Django's built-in tools.

## Consequences
Unauthenticated users are redirected to the login page before they can access program management routes. The trade-off is that this protects login access only; a more advanced production app would also add detailed organisation membership permissions.

## Evidence in current implementation
- `ProgramManageListView`, `ProgramCreateView`, `ProgramUpdateView`, and `ProgramDeleteView` use `LoginRequiredMixin`.
- `project_blog/settings.py` defines `LOGIN_URL`.
- `accounts/views.py` and `accounts/urls.py` provide registration, login, and logout flow.

<!-- ADDED FOR HIT237 FEEDBACK: revision history for living-document criterion -->
## Revision history
| Date | Change |
|---|---|
| 2026-05-26 | Added ADR for authentication and CRUD access control feedback. |
