# ADR: Separate logic from presentation

## Status
Accepted

## Context
The project must include a browsable public site and a management area for CRUD. It also needs to remain understandable for beginner-level Django development. Mixing HTML presentation with query logic or validation logic would make the code harder to maintain and harder to justify architecturally.

## Alternatives considered

### Option 1: Put most logic directly in templates or views
**Pros**
- Easy to start quickly
- Fewer files at the beginning

**Cons**
- Poor separation of concerns
- Harder to test and maintain
### Option 2: Keep data rules in models/managers, input structure in forms, request handling in views, and display in templates
**Pros**
- Cleaner architecture
- Better separation of concerns
- Easier to maintain
- Better alignment with rubric expectations

**Cons**
- Requires more files
- Requires clearer planning

## Decision
The project separates responsibilities across Django layers:
- models handle data structure and validation
- managers handle reusable query logic
- forms handle structured user input
- views coordinate requests and responses
- templates handle display

## Rationale
This structure is easier to understand and explain. It also supports object-oriented decomposition and keeps the user interface cleaner.

## Code reference
- `youthjustice_app/models.py`
- `youthjustice_app/managers.py`
- `youthjustice_app/forms.py`
- `youthjustice_app/views.py`
- `youthjustice_app/templates/youthjustice_app/base.html`

## Consequences
The application is more maintainable and better structured. The trade-off is that the team must manage several files instead of placing everything in one location.