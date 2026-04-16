# ADR: Use a separate Organisation model linked to Program

## Status
Accepted

## Context
The application needs to store youth diversion and support programs. In earlier thinking, organisation information could be stored as plain text inside `Program`, but that would not model the real-world relationship accurately. One organisation can offer multiple programs.

## Alternatives considered

### Option 1: Keep organisation as a plain text field in Program
**Pros**
- Very simple
- Easy for beginners to implement

**Cons**
- Repeats organisation data
- Harder to maintain consistency
- Weak relationship modelling

### Option 2: Create a separate Organisation model and link Program using a ForeignKey
**Pros**
- Represents the domain more accurately
- Reduces duplicate data
- Better supports rubric expectations around relationships

**Cons**
- Requires a migration
- Slightly more complexity

## Decision
The project uses a separate `Organisation` model, and each `Program` links to an organisation with a `ForeignKey`.

## Rationale
This improves data integrity and gives the application a clearer one-to-many relationship in the main business domain.

## Code reference
- `youthjustice_app/models.py` — `Organisation`
- `youthjustice_app/models.py` — `Program.organisation`
- `youthjustice_app/forms.py` — `ProgramForm`
- `youthjustice_app/views.py` — `select_related("organisation")`

## Consequences
The core model design is cleaner and easier to document in the ERD. The trade-off is that organisation records must exist before creating related programs.