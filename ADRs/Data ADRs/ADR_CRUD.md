# ADR: Separate public browsing pages from management CRUD pages

## Status
Accepted

## Last updated
2026-05-26

## Context
The application needs both a public interface for browsing programs and a way to demonstrate Create, Read, Update, and Delete functionality. Mixing CRUD controls directly into the public pages would make the interface more cluttered and harder to explain.

## Alternatives considered

### Option 1: Put CRUD controls directly in public pages
**Pros**
- Fewer pages
- Everything visible in one place

**Cons**
- Public interface becomes cluttered
- Harder to separate browsing from maintenance

### Option 2: Create a separate management area for CRUD
**Pros**
- Clear separation of concerns
- Cleaner public site
- Easier to understand architecture framework

**Cons**
- Requires more routes and templates

## Decision
The project keeps public browsing pages separate from program management pages.

## Rationale
This makes the public site simpler while still demonstrating full CRUD functionality for assessment purposes.

## Code reference
- `youthjustice_app/urls.py`
- `youthjustice_app/views.py`
- `youthjustice_app/templates/youthjustice_app/manage_programs.html`
- `youthjustice_app/templates/youthjustice_app/add_program.html`
- `youthjustice_app/templates/youthjustice_app/edit_program.html`
- `youthjustice_app/templates/youthjustice_app/delete_program.html`

## Consequences
The interface is easier to understand and explain. The trade-off is a slightly larger number of templates and routes.