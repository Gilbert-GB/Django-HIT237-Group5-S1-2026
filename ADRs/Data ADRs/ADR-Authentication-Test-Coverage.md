# ADR: Authentication Test Coverage

## Status
Accepted

## Date created
2026-05-26

## Last updated
2026-05-26

## Context
The project uses Django authentication for login, registration, logout, and access protection on management pages. These behaviours are important because the application separates public browsing from authenticated program management.

## Decision
Add simple tests for the existing accounts app authentication flow. The tests check that the login page loads, registration creates and logs in a user, and logout redirects back to the login page.

## Consequences
The authentication flow is easier to verify during marking without adding complex role or permission logic. The trade-off is that these tests cover the basic student-project auth flow only, not advanced production security scenarios.

## Evidence in current implementation
- `accounts/tests.py` tests login page rendering.
- `accounts/tests.py` tests registration and automatic login.
- `accounts/tests.py` tests the custom logout redirect.
- `youthjustice_app/tests.py` tests login protection for the program management page.
