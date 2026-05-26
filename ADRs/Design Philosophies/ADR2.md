# ADR: Use Django's Less Code philosophy

## Status
Accepted

## Last updated
2026-05-26

## Context
The application needs multiple pages, CRUD functionality, model validation, filtering, and dashboard data handling. Repeating logic across files would make the project harder to maintain and harder to explain in viva.

## Alternatives considered

### Option 1: Repeat logic in multiple views and templates
**Pros**
- Simple to start with
- Easy to write small isolated features quickly

**Cons**
- Duplicated code
- Harder to maintain
- Harder to explain as good architecture

### Option 2: Reuse Django features such as ModelForms, custom managers, and class-based views
**Pros**
- Less repeated code
- Cleaner separation of concerns
- Easier to extend later
- Better alignment with Django philosophy

**Cons**
- Requires more understanding of Django abstractions
- Slightly more structured design

## Decision
The project adopts Django’s Less Code philosophy by using `ModelForm` for program input handling, reusable manager methods for common queries, and generic class-based views for CRUD pages.

## Rationale
This choice reduced repeated logic across the project. It also made the system easier to maintain, because changes to model validation, query logic, or form structure could be made in one place instead of many.

## Code reference
- `youthjustice_app/forms.py`
- `youthjustice_app/managers.py`
- `youthjustice_app/views.py`

## Consequences
The codebase became cleaner and more reusable. The trade-off is that the team had to understand how Django forms, managers, and generic views work together.