# ADR: QuerySet Composition and Custom Managers

## Status
Accepted

## Date created
2026-05-26

## Last updated
2026-05-26

## Context
The feedback asked for stronger QuerySet composition through custom managers and annotations or aggregations. The application already has manager methods and view/service queries that keep repeated query logic organised.

## Decision
Use custom managers in `youthjustice_app/managers.py` for common program, crime, and engagement queries. This lets views call readable methods such as `Program.objects.available()`, `Program.objects.search(query)`, and `CrimeData.objects.total_by_region()`.

## Consequences
The views stay easier to read because common filters and grouped totals live in the manager layer. The trade-off is that students need to know where manager methods are defined.

## Evidence in current implementation
- `ProgramManager.available()` and `ProgramManager.search()` support reusable program filtering.
- `CrimeDataManager.total_by_region()`, `total_by_year()`, and `total_by_category()` use `values()` and `annotate(Sum())`.
- Organisation and region summaries in `views.py` use `Count`, while engagement summaries use `Avg`.
- `EngagementDataManager.nt_trend()` provides a reusable engagement trend query.