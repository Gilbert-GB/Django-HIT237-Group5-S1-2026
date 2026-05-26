# ADR: Functionality Improvements — Assessment 4

## Status
Accepted

## Last updated
2026-05-26

---

## Context
After completing the initial build of the Youth Justice NT application (Assessment 2/3), the system had basic functionality: a program directory with search and filtering, a crime data dashboard, data import pipeline, and user authentication. However, several functional gaps existed that limited the system's usefulness as a real-world tool.

The teaching team specifically requested **better functionality over better visuals**. This ADR documents the 10 functional improvements implemented for Assessment 4, the reasoning behind each, and how they align with the team's existing design philosophies.

---

## Decision
We implemented **10 targeted functionality improvements** across the application, focusing on features that add real utility for users (public visitors, researchers, government staff) without introducing unnecessary complexity.

---

## Improvement 1: Pagination on Programs Page

### Problem
All programs loaded on a single page. With a growing directory, this creates slow page loads and poor user experience. Pagination is a basic expected feature of any listing page.

### Solution
Added Django's built-in `Paginator` to the `programs` view, displaying 9 programs per page (3×3 grid). Pagination links preserve all active filters (search, region, category, sort, age) across page transitions using GET parameters.

### Implementation
- **Views:** Added `Paginator` and `page_obj` to the `programs` view
- **Templates:** Added pagination navigation with First/Prev/Page Numbers/Next/Last links
- **Filter preservation:** Every pagination link includes `{% if search_query %}&search={{ search_query }}{% endif %}` for all active filters

### Alignment
- **Less Code (ADR2):** Uses Django's built-in `Paginator` class — zero external libraries
- **Quick Development (ADR1):** 3 lines of Python + template block, fully functional pagination

---

## Improvement 2: Engagement Data Dashboard

### Problem
370 Closing the Gap engagement records were imported into the database but had zero visibility. No views, no API, no charts. An entire dataset was sitting unused while only crime data appeared on the dashboard.

### Solution
Built a complete `/engagement/` page with:
- 3 interactive filters (year, sex, indigenous status)
- 4 KPI cards (latest year, Indigenous NT rate, Non-Indigenous NT rate, gap)
- 3 Chart.js charts: NT vs National trend line, comparison by sex (grouped bar), comparison by indigenous status (horizontal bar)
- JSON API endpoint at `/api/engagement/` for dynamic chart updates

### Implementation
- **Views:** `engagement_page` (renders template) and `engagement_data` (returns filtered JSON)
- **Templates:** New `engagement.html` with Chart.js integration
- **URLs:** Two new routes — `/engagement/` and `/api/engagement/`
- **Filters:** Year dropdown auto-populates from available data, sex and indigenous status filters apply server-side

### Alignment
- **Separate Logic from Presentation (ADR3):** API endpoint handles data logic, template handles display, Chart.js handles visualisation
- **Data Pipeline ADR:** This is the presentation layer for the engagement data that the pipeline imported

---

## Improvement 3: Age Filter on Programs Page

### Problem
The `ProgramManager` already had a `for_age()` method that filters programs by a given age, but no view or template used it. Users could not search for programs that accept a specific age (e.g., "show me programs for a 14-year-old").

### Solution
Added an age input field to the programs page filter bar. Users enter an age number, and the system filters programs where `age_min <= entered_age` and `age_max >= entered_age`. The age filter works alongside all existing filters (search, region, category, sort) and is preserved across pagination.

### Implementation
- **Views:** Added `selected_age` parameter extraction and age filtering logic
- **Templates:** Added `<input type="number" name="age">` to the filter form
- **Pagination:** Added `{% if selected_age %}&age={{ selected_age }}{% endif %}` to all pagination links

### Alignment
- **Less Code (ADR2):** 6 lines of view logic, 1 line of template HTML
- **Data Encapsulation ADR:** Uses the model's age fields with ORM's `__lte` and `__gte` lookups

---

## Improvement 4: Login Protection on CRUD Views

### Problem
All program management views (add, edit, delete, manage list) were publicly accessible. Anyone could visit `/manage/programs/add/` and create a program without logging in. This is a security gap.

### Solution
Added `LoginRequiredMixin` as the first parent class on all four CRUD class-based views. Added `LOGIN_URL` setting to redirect unauthenticated users to the login page. After login, Django automatically redirects users back to the page they originally tried to access.

### Implementation
- **Views:** Added `LoginRequiredMixin` to `ProgramManageListView`, `ProgramCreateView`, `ProgramUpdateView`, `ProgramDeleteView`
- **Settings:** Added `LOGIN_URL = "/accounts/login/"` to `settings.py`

### Alignment
- **Quick Development (ADR1):** `LoginRequiredMixin` is a built-in Django mixin — one word added per view
- **Authentication ADR:** Complements the existing auth system by protecting management routes

---

## Improvement 5: DashboardService Integration

### Problem
`dashboard_service.py` contained a full `DashboardService` class with methods for monthly trends, top regions, category breakdowns, alcohol stats, DV stats, top offences, and KPIs. However, the `dashboard_data` view in `views.py` rewrote all these queries from scratch. The service layer was dead code.

### Solution
Refactored `dashboard_data` to use `DashboardService` methods for the default (unfiltered) dashboard view. When filters are active, inline queries are used because `DashboardService` methods don't accept filter parameters. The response now also includes an `extra` block exposing yearly trends, alcohol stats, DV stats, and top offences — data that `DashboardService` already computed but was never exposed.

### Implementation
- **Views:** Refactored `dashboard_data` to import and use `DashboardService` for unfiltered data
- **Response:** Added `extra` key in JSON response with 4 additional datasets

### Alignment
- **Less Code (ADR2):** Eliminated duplicated query logic between views.py and dashboard_service.py
- **Separate Logic from Presentation (ADR3):** Query logic stays in the service layer, the view only decides which data to return

---

## Improvement 6: Organisation List and Detail Pages

### Problem
The `Organisation` model existed with a `ForeignKey` relationship to `Program` (one organisation manages many programs), but there were no views to browse organisations or see all programs under one organisation. The model relationship was invisible to users.

### Solution
Built two new pages:
- `/organisations/` — lists all organisations as cards with their type, description, program count, and contact info. Filterable by organisation type (Government, Non-profit, Community, Education, Other).
- `/organisations/<id>/` — detail page for one organisation showing full contact info, total vs available program counts, and a grid of all programs from that organisation.

### Implementation
- **Views:** `organisation_list` (with `annotate(program_count=Count("programs"))`) and `organisation_detail` (using `related_name="programs"`)
- **Templates:** Two new templates — `organisations.html` and `organisation_detail.html`
- **URLs:** Two new routes
- **Navigation:** Added "Organisations" link to navbar

### Alignment
- **Model Relationships ADR:** Demonstrates the Organisation → Program FK relationship in the UI
- **Less Code (ADR2):** Uses Django's `annotate()` and `related_name` — no manual counting or extra queries

---

## Improvement 7: Related Programs on Program Detail Page

### Problem
When viewing a program's detail page, there was no way to discover similar programs. Users had to go back to the listing and search again. This breaks natural browsing flow and misses an opportunity to increase engagement.

### Solution
Added two "related programs" sections below the main program info:
- **"Other Programs in [Region]"** — up to 4 available programs in the same region, excluding the current one
- **"More [Category] Programs"** — up to 4 available programs in the same category, excluding the current one and any already shown in the region section (no duplicates)

### Implementation
- **Views:** Expanded `program_detail` to query `same_region` and `same_category` querysets with `exclude(pk=program.pk)` and `exclude(pk__in=shown_ids)` to prevent duplicates
- **Templates:** Added two grid sections after the main detail card, each showing compact program cards

### Alignment
- **Data Encapsulation ADR:** Uses `Program.objects.available()` manager method for filtering
- **Quick Development (ADR1):** Simple ORM queries with `filter()`, `exclude()`, and slicing `[:4]`

---

## Improvement 8: CSV Export for Filtered Data

### Problem
Users (especially researchers and government staff) could view data on the website but could not download it. There was no way to extract filtered programs, crime data, or engagement data for offline analysis, reporting, or sharing.

### Solution
Built three CSV export endpoints that respect all active filters:
- `/export/programs/` — exports filtered programs with name, organisation, region, category, age range, availability, description, website
- `/export/crime/` — exports filtered crime data with year, month name, region, offence category/type, alcohol/DV involvement, count
- `/export/engagement/` — exports filtered engagement data with year, sex, indigenous status, NT value, national value, calculated gap

Each endpoint uses the same filter parameters as its corresponding page, so the downloaded CSV matches exactly what the user sees on screen. Export buttons were added to the programs page, crime dashboard, and engagement dashboard.

### Implementation
- **Views:** Three new view functions using Python's built-in `csv` module and `HttpResponse` with `content_type="text/csv"`
- **Templates:** Export buttons added to programs.html, dashboard.html, and engagement.html with JavaScript functions to pass current filter values
- **URLs:** Three new routes under `/export/`
- **Model Properties:** Export views use `@property` methods from models (e.g., `month_name`, `offence_category_short`, `gap_display`) for clean formatted output

### Alignment
- **Less Code (ADR2):** Uses Python's built-in `csv.writer` — no pandas, no external libraries
- **Data Encapsulation ADR:** Exports use model properties for formatting, not raw values

---

## Improvement 9: Enhanced Homepage with Real Data

### Problem
The homepage only showed three program count numbers (Total, Featured, Available). With 6,574 crime records and 370 engagement records in the database, the homepage wasted the opportunity to give users an overview of the system's full data.

### Solution
Expanded the homepage to show five data sections:
1. **Program stats** (existing) — Total, Featured, Available
2. **NT Data Highlights** (new) — Total recorded offences, most common offence, Indigenous youth engagement rate, engagement gap
3. **Crime by Region** (new) — Top 5 regions by offence count, clickable to region profiles
4. **Programs by Region** (new) — Program count per region, clickable to pre-filtered program list
5. **Quick links** (new) — Styled cards linking to Crime Dashboard and Engagement Data pages

### Implementation
- **Views:** Expanded `home` view with crime aggregation queries (`Sum`, `Count`), engagement data lookups, and programs-per-region grouping with display name mapping
- **Templates:** Added four new sections to `home.html` with stat cards, region cards, and navigation cards

### Alignment
- **Separate Logic from Presentation (ADR3):** All data aggregation happens in the view, template only displays
- **Data Pipeline ADR:** Homepage now surfaces data from both imported datasets, proving the pipeline's value

---

## Improvement 10: Region Profile Pages

### Problem
Data about each NT region was scattered across different pages — programs were on the programs page, crime data was on the dashboard, engagement data was on the engagement page. There was no way to see a complete picture of one region. This is the most important view for someone working in a specific area.

### Solution
Built a comprehensive region profile page at `/region/<slug>/` that combines all three datasets for one region:
- **5 KPI cards** — programs available, total offences, alcohol-related %, DV-related %, engagement gap
- **3 Chart.js charts** — offences by year (bar), offence categories (horizontal bar), monthly crime trend (line)
- **Programs by category breakdown** — clickable cards linking to pre-filtered programs
- **Program cards** — first 6 programs with "View All" button
- **CSV export buttons** — download crime or program data for this specific region
- **Region navigation** — pill buttons to switch between regions
- **Region ranking** — shows the region's rank among all regions by total offence count

### Implementation
- **Views:** New `region_profile` view with region slug validation, crime region name mapping (program slugs like "alice_springs" → crime CSV names like "Alice Springs"), aggregation queries for crime, programs, and engagement
- **Templates:** New `region_profile.html` extending base.html with Chart.js embedded using Django template variables
- **URLs:** New route `/region/<str:region_slug>/`
- **Cross-linking:** Homepage crime-by-region cards link to region profiles; region profiles link to filtered programs page and export endpoints

### Alignment
- **All ADRs:** This feature integrates every design philosophy — built-in Django features (Quick Development), minimal code for maximum output (Less Code), clean view/template separation (Separate Logic), model managers and properties for data access (Encapsulation), and imported pipeline data (Pipeline ADR)

---

## Files Changed / Added

```
youthjustice_app/
├── views.py                                    # MODIFIED — 10 new/updated view functions
├── urls.py                                     # MODIFIED — 9 new URL routes added
├── templates/
│   └── youthjustice_app/
│       ├── home.html                           # MODIFIED — enhanced with data sections
│       ├── programs.html                       # MODIFIED — pagination, age filter, export
│       ├── program_detail.html                 # MODIFIED — related programs sections
│       ├── dashboard.html                      # MODIFIED — export button
│       ├── base.html                           # MODIFIED — new nav links
│       ├── engagement.html                     # NEW — engagement dashboard
│       ├── organisations.html                  # NEW — organisation listing
│       ├── organisation_detail.html            # NEW — organisation detail
│       └── region_profile.html                 # NEW — region profile page

project_blog/
└── settings.py                                 # MODIFIED — added LOGIN_URL
```

### New URL Routes Added
| Route | View | Purpose |
|-------|------|---------|
| `/engagement/` | `engagement_page` | Engagement data dashboard |
| `/api/engagement/` | `engagement_data` | Engagement JSON API |
| `/organisations/` | `organisation_list` | Browse organisations |
| `/organisations/<pk>/` | `organisation_detail` | Organisation detail |
| `/region/<slug>/` | `region_profile` | Region profile page |
| `/export/programs/` | `export_programs_csv` | Download programs CSV |
| `/export/crime/` | `export_crime_csv` | Download crime data CSV |
| `/export/engagement/` | `export_engagement_csv` | Download engagement CSV |

---

## Consequences

### Positive
1. **Complete data utilisation** — all three datasets (programs, crime, engagement) are now visible, filterable, exportable, and interconnected
2. **Real-world utility** — CSV exports, age-based search, and region profiles serve actual user needs (researchers, government staff, community workers)
3. **Security improvement** — CRUD operations are now protected behind authentication
4. **Zero dead code** — DashboardService is wired into views, engagement data has full UI
5. **Cross-referencing** — region profiles prove the three datasets work together, not in silos
6. **No new dependencies** — every feature uses Django built-ins and Chart.js CDN

### Negative
1. `views.py` is significantly larger — could benefit from splitting into separate view modules in future
2. Region profiles assume engagement data is NT-wide (not per-region), which is a data limitation, not a code limitation
3. Chart.js is loaded from CDN on multiple pages — could be moved to base.html for caching

---

## Team Contribution
- **Mahathir Md Taief:** All 10 functionality improvements — views, templates, URL routing, export logic, and this ADR

---
## Alignment with Other ADRs
- **ADR: Quick Development** — All features implemented using Django's built-in tools and Python standard library. No external dependencies added.
- **ADR: Less Code** — Each improvement focuses on maximum functionality with minimal code. For example, CSV exports use `csv.writer` instead of pandas, and pagination uses Django's `Paginator` class.

