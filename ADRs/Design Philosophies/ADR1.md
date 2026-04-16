# ADR: Use Django's Quick Development philosophy

## Status
Accepted

## Context
The project is a student-built Django web application that must demonstrate architectural thinking, object-oriented design, and supporting documentation within a limited assessment timeframe. The team needed an approach that allowed functional progress quickly without building low-level infrastructure manually.

## Alternatives considered

### Option 1: Build more functionality manually from scratch
**Pros**
- Greater low-level control
- More custom implementation choices

**Cons**
- Slower development
- More repeated code
- Higher risk of unfinished features within the deadline

### Option 2: Use Django’s built-in structure and rapid development features
**Pros**
- Faster development
- Clear project/app structure
- Built-in support for models, forms, views, templates, admin, and routing
- More time available for design decisions and documentation

**Cons**
- Less low-level control
- Requires understanding Django conventions

## Decision
The project adopts Django’s Quick Development philosophy by using Django’s built-in project structure, model-driven forms, routing, templates, and admin support to scaffold the application quickly.

## Rationale
This approach was appropriate because the assessment emphasises design rationale and architecture rather than writing every part manually. Using Django’s framework support allowed the team to focus on modelling the youth justice problem, structuring CRUD functionality, and documenting design choices.

## Code reference
- `project_blog/urls.py`
- `youthjustice_app/models.py`
- `youthjustice_app/forms.py`
- `youthjustice_app/views.py`
- `youthjustice_app/admin.py`

## Consequences
The project was able to progress faster and maintain a clearer structure. The trade-off is that the team had to follow Django conventions closely, but this also improved consistency and maintainability.