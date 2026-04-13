# ADR: Data Encapsulation in Pipeline Models

## Context
After building the data import pipeline (see ADR_Pipeline.md), we had two new models — `CrimeData` and `EngagementData` — storing 6,574 crime records and 370 engagement records respectively.

However, these models were just plain data containers. The fields stored raw values directly from the CSV files with no protection, no formatting, and no reusable query logic. This created several problems:

- **No validation:** A crime record could be saved with month = 15 or count = -200. An engagement percentage could be saved as 500%. The database would accept anything.
- **Raw values in templates:** The crime CSV stores months as numbers (1, 2, 3). Templates had to figure out how to display "January" instead of "1". Offence categories like "02 Assault" include a number prefix that should not be shown to users.
- **Repeated query logic:** Every view that needed crime totals by region had to write the same `.values("region").annotate(total=Sum("count"))` query. The same aggregation code was duplicated in views.py and dashboard_service.py.
- **No computed insights:** The Closing the Gap data has both NT and national values, but the gap between them (how far NT is behind) was not calculated anywhere — each view or template had to do the maths itself.

These problems violate the team's existing design philosophies. Repeated queries break "Less Code" (ADR2). Formatting logic in templates breaks "Separate Logic from Presentation" (ADR3).

---

## Decision
We will apply **data encapsulation** to both pipeline models by adding three layers of protection and logic inside the models themselves:

1. **Validation rules** — models reject invalid data before saving
2. **Computed properties** — models provide formatted and calculated values
3. **Custom query managers** — models encapsulate common database queries

---

## What Was Added

### CrimeData Model

**Validation (`clean` method):**
| Rule | What it prevents |
|------|-----------------|
| Year must be 2000 or later | Blocks nonsense years like 0 or 1800 |
| Month must be 1–12 | Blocks invalid months like 0 or 15 |
| Count cannot be negative | Blocks values like -50 offences |

**Properties:**
| Property | What it returns | Example |
|----------|----------------|---------|
| `month_name` | Month number as readable name | 3 → "March" |
| `period_display` | Formatted period string | "March 2024" |
| `is_alcohol_related` | Whether alcohol was involved | True / False |
| `is_dv_related` | Whether domestic violence was involved | True / False |
| `offence_category_short` | Category without number prefix | "02 Assault" → "Assault" |

**Custom Manager (`CrimeDataManager`):**
| Method | What it does | Replaces |
|--------|-------------|----------|
| `by_region("Darwin")` | Filters by region | `.filter(region="Darwin")` |
| `by_year(2024)` | Filters by year | `.filter(year=2024)` |
| `by_offence("02 Assault")` | Filters by offence category | `.filter(offence_category=...)` |
| `total_by_region()` | Sum of offences grouped by region | `.values("region").annotate(total=Sum("count"))` |
| `total_by_year()` | Sum of offences grouped by year | `.values("year").annotate(total=Sum("count"))` |
| `total_by_category()` | Sum of offences grouped by category | `.values("offence_category").annotate(...)` |

---

### EngagementData Model

**Validation (`clean` method):**
| Rule | What it prevents |
|------|-----------------|
| Year must be 2000 or later | Blocks nonsense years |
| NT value must be 0–100 | Blocks impossible percentages like 500% |
| National value must be 0–100 | Same protection for national values |

**Properties:**
| Property | What it returns | Example |
|----------|----------------|---------|
| `nt_display` | NT value as formatted percentage | 41.0 → "41.0%" |
| `national_display` | National value as formatted percentage | 57.3 → "57.3%" |
| `gap` | Difference between NT and national | 41.0 - 57.3 = -16.3 |
| `gap_display` | Gap with sign | "-16.3%" |
| `is_below_national` | Whether NT is below national average | True / False |
| `is_indigenous` | Whether record is for Indigenous people | True / False |

**Custom Manager (`EngagementDataManager`):**
| Method | What it does |
|--------|-------------|
| `by_year(2021)` | Filters by specific year |
| `indigenous_only()` | Returns only Indigenous records |
| `non_indigenous_only()` | Returns only non-Indigenous records |
| `by_sex("Males")` | Filters by sex |
| `nt_trend()` | Returns NT values over time for Indigenous people (for charts) |

---

## Alternatives Considered

### 1. Keep models as plain data containers, handle everything in views
**Pros:** Models stay simple and short.
**Cons:** Validation logic, formatting, and queries get scattered across views.py, dashboard_service.py, and templates. Same code is repeated in multiple places. If a rule changes, every file must be updated. This directly violates "Less Code" and "Separate Logic from Presentation."

### 2. Create separate utility/helper files for validation and formatting
**Pros:** Logic is at least in one place.
**Cons:** Adds extra files that are disconnected from the models. Django already provides the right tools (clean, property, Manager) — creating separate utilities ignores Django's built-in patterns and adds unnecessary complexity.

### 3. Put validation, properties, and query logic inside the models (Chosen)
**Pros:**
- Each model is self-contained — it validates, formats, and queries its own data
- Views become shorter — they call manager methods instead of writing raw queries
- Templates become cleaner — they use properties instead of doing formatting
- One place to update — if a rule or format changes, only models.py is modified
- Follows Django's recommended patterns (clean, property, Manager)

**Cons:**
- models.py file is now longer
- `clean()` validation does not run during `bulk_create()` — this is intentional for pipeline performance, since the import commands already validate data during the reading step

---

## Rationale
This decision aligns with all existing team ADRs:

- **Quick Development (ADR1):** `clean()`, `@property`, and custom `Manager` are all built-in Django features. Zero extra libraries installed.
- **Less Code (ADR2):** Views no longer repeat the same filter and annotate queries. Manager methods like `total_by_region()` replace 4 lines of queryset code with 1 method call.
- **Separate Logic from Presentation (ADR3):** All data logic (validation, calculations, formatting) is now inside models.py. Templates only display values. Views only connect models to templates.
- **Data Pipeline ADR:** The pipeline imports raw CSV data. Encapsulation adds the intelligence layer on top — raw data goes in, validated and formatted data comes out.

---

## Code References

```text
youthjustice_app/models.py

Classes added/modified:
- CrimeDataManager     (custom manager with 6 query methods)
- CrimeData            (clean + 5 properties)
- EngagementDataManager (custom manager with 5 query methods)
- EngagementData        (clean + 6 properties)
```

---
**This ADR can be updated as the project development progresses.**
