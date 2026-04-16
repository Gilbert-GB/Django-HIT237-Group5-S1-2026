# ADR: Move custom managers into a separate managers.py file

## Status
Accepted

## Context
As the project grows, custom QuerySet and manager methods for multiple models can make `models.py` too large and harder to read. The team wanted a cleaner layout that still keeps query logic near the model layer.

## Alternatives considered

### Option 1: Keep all manager code inside models.py
**Pros**
- Fewer files
- Easy to see model and manager together

**Cons**
- Large `models.py`
- Harder readability
- Harder to navigate

### Option 2: Move custom managers into managers.py
**Pros**
- Cleaner project structure
- Easier readability
- Better separation of responsibilities

**Cons**
- One extra file
- Requires imports between files

## Decision
Custom managers are defined in `managers.py` and imported into the models.

## Rationale
This keeps the models easier to read while still preserving reusable query logic in the model layer.

## Code reference
- `youthjustice_app/managers.py`
- `youthjustice_app/models.py`

## Consequences
The project becomes easier to navigate. The trade-off is slightly more file coordination during development.