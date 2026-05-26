# ADR: Dashboard Service and Data Aggregation

## Status
Accepted

## Date created
2026-05-26

## Last updated
2026-05-26

## Context
The application dashboard needs totals, trends, top regions, crime categories, alcohol statistics, domestic violence statistics, and top offences. These values require repeated aggregation queries.

## Decision
Keep dashboard aggregation logic in `youthjustice_app/dashboard_service.py` where possible, and return JSON from the existing dashboard API views without changing the dashboard templates, JavaScript, URLs, charts, or response structure.

## Consequences
The dashboard has a simple service layer for reusable aggregation queries. The trade-off is that some filtered dashboard logic still stays in the view so the current dashboard behaviour remains stable.

## Evidence in current implementation
- `DashboardService.get_monthly_trend()` uses `values()` and `annotate(Sum())`.
- `DashboardService.get_top_regions()` and `get_category_breakdown()` provide chart-ready grouped data.
- `dashboard_data` in `youthjustice_app/views.py` keeps the existing JSON keys used by the dashboard JavaScript.

## Revision history
| Date | Change |
|---|---|
| 2026-05-26 | Added ADR for dashboard service and aggregation feedback. |
