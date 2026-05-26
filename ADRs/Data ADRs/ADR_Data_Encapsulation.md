## Architecture Decision Record (ADR) for:
### _Design Philosophy : Data Encapsulation_
## Status
Accepted

## Last updated
2026-05-26

## Introduction

### Prologue (Summary):
In the context of building our Youth Justice NT web application, our team needed to ensure that our Django models are not just simple data containers but also protect and manage their own data. Following the principle of **Data Encapsulation**, we decided to add validation rules, computed properties, helper methods, and custom managers inside the models themselves, rather than scattering this logic across views and templates. This keeps our data safe, our code organised, and makes the application easier to maintain.

### Discussion (Context):
Without encapsulation, our models were just raw database fields with no protection. Any part of the code could put bad data into the database, and business logic was mixed into views and templates.

Problems we faced without encapsulation:
- A program could be saved with `age_min = 20` and `age_max = 10` (minimum bigger than maximum) and Django would not stop it
- Crime data could be saved with a negative offence count, which makes no sense
- Engagement data percentages could be saved as 500%, which is impossible
- Views had to repeat the same filter queries everywhere (e.g., `Program.objects.filter(is_available=True)` written in multiple places)
- Templates were doing formatting logic like calculating age ranges, when the model should handle that
- If a program was marked as unavailable, it could still remain featured — there was no rule to prevent this

These are all signs of missing encapsulation — the model does not control or protect its own data.

### Solutions (Decision):
We applied data encapsulation to all three models (Program, CrimeData, EngagementData) using four Django techniques:

**1. Validation via `clean()` method**
Each model now validates its own data before saving. Django calls `clean()` automatically in forms and admin. If the data is invalid, it raises a `ValidationError` and the record is not saved.

Examples:
- Program: `age_min` cannot be greater than `age_max`, ages must be between 0 and 25
- CrimeData: month must be 1–12, count cannot be negative
- EngagementData: percentage values must be between 0 and 100

**2. Computed properties via `@property`**
Instead of doing calculations in templates or views, the model provides ready-made values.

Examples:
- `program.age_range_display` returns "10 - 17 years" instead of the template formatting it
- `crime.month_name` converts month number 3 to "March"
- `crime.offence_category_short` converts "02 Assault" to just "Assault"
- `engagement.gap` calculates the difference between NT and national values
- `engagement.nt_display` returns "41.0%" instead of the template formatting the number

**3. Helper methods**
Models can perform actions on themselves with built-in business rules.

Examples:
- `program.mark_unavailable()` sets `is_available = False` AND automatically removes `is_featured` too (business rule: featured programs must be available)
- `program.mark_available()` sets the program back to available

**4. Custom Managers**
Instead of writing raw `.filter()` queries in every view, we created manager classes that encapsulate common queries inside the model.

Examples:
- `Program.objects.available()` instead of `Program.objects.filter(is_available=True)`
- `Program.objects.search("mentoring")` instead of writing Q objects in views
- `CrimeData.objects.total_by_region()` instead of writing `.values().annotate()` in views
- `EngagementData.objects.indigenous_only()` instead of filtering by the long status string everywhere

### Consequences (Results):
Positive attributes:
1. Data integrity is guaranteed — bad data cannot enter the database
2. Business rules are enforced consistently (e.g., featured programs must be available)
3. Views and templates are cleaner — they just call model properties and manager methods
4. Code duplication is reduced — common queries are written once in the manager
5. Easier to maintain — if a rule changes, we update it in one place (the model) not in every view

Negative attributes:
1. Models are longer and more complex than before
2. Team members need to understand properties and custom managers
3. The `clean()` validation only runs automatically in forms/admin — when using `bulk_create()` in the pipeline, validation is skipped for performance (this is intentional and acceptable for trusted CSV data from government sources)

---

## Code References

```text
youthjustice_app/models.py

Encapsulation applied to:
- Program model       → clean(), @property, helper methods, ProgramManager
- CrimeData model     → clean(), @property, CrimeDataManager
- EngagementData model → clean(), @property, EngagementDataManager
```

---

## Alignment with Other ADRs

- **ADR: Quick Development** — Custom managers and properties are built-in Django features. No extra libraries needed.
- **ADR: Less Code** — Views become shorter because query logic moves into managers. Templates become simpler because formatting moves into properties.
- **ADR: Separate Logic from Presentation** — Business logic (validation, calculations, queries) stays in models.py. Templates only display data. Views only connect the two.

---
**This ADR can be updated as the project development progresses.**