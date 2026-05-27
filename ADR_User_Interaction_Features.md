# ADR: User Interaction Features Improvements - Assessment 4

## Status
Accepted

---

## Context

After the initial build of the Youth Justice NT application, the system already allowed users to browse programs, search and filter results, view dashboards, and manage program records. However, the program directory still worked mostly as an information display system.

For Assessment 4, the focus was to improve functionality instead of only improving visuals. The program directory needed more user interaction so users could take useful actions while browsing programs.

Users may need to request help, report incorrect information, compare programs, save useful programs, or share a program link with someone else.

---

## Decision

I implemented user interaction features to make the program directory more practical and useful.

The improvements include:

1. User request and report functionality
2. Request status tracking
3. Program comparison
4. Program bookmark functionality
5. Saved program count in the navigation bar
6. Program link sharing

These features were added using Django models, forms, views, URLs, templates, sessions, admin registration, and simple JavaScript.

---

## Improvement 1: User Request and Report Functionality

### Problem

Users could browse programs, but they had no simple way to ask for help about a program or report incorrect program information.

### Solution

Added a Requests page where users can submit help requests and report outdated or incorrect program details.

### Implementation

- Added `HelpRequest` and `ProgramInfoReport` models
- Added `HelpRequestForm` and `ProgramInfoReportForm`
- Added `requests_page` view
- Added `requests.html`
- Registered request and report models in Django admin

### Alignment

- Uses Django ModelForms and admin support
- Keeps request and report data in proper models
- Separates form logic from template display

---

## Improvement 2: Request Status Tracking

### Problem

After submitting a help request, users needed a way to check the status of their request.

### Solution

Added simple status tracking using request ID and email. Users can check whether their request is new, in review, contacted, or closed.

### Implementation

- Added status choices to the `HelpRequest` model
- Added lookup logic in `requests_page`
- Displayed request status on the Requests page
- Allowed staff to update status through Django admin

### Alignment

- Uses existing request data
- Avoids a complex user account tracking system
- Keeps the feature simple and easy to test

---

## Improvement 3: Program Comparison

### Problem

Users could browse and filter programs, but they could not compare programs side by side.

### Solution

Added a comparison page where users can compare selected programs based on organisation, region, category, age range, availability, description, and website.

### Implementation

- Added `compare_programs` view
- Added `compare_programs.html`
- Added `/compare/` route
- Added “Compare This Program” action on program cards

### Alignment

- Uses existing `Program` data
- No new model was needed
- Uses simple GET parameters for selected programs

---

## Improvement 4: Program Bookmarks

### Problem

Users could find useful programs, but they had no way to save them for later.

### Solution

Added bookmark functionality so users can save and remove programs. Saved programs can be viewed from the Saved page.

### Implementation

- Added `add_bookmark`, `remove_bookmark`, and `bookmarks_page` views
- Added `bookmarks.html`
- Added bookmark routes
- Stored saved program IDs in Django sessions

### Alignment

- Uses Django sessions instead of adding another database table
- Keeps the feature simple
- Supports better user browsing

---

## Improvement 5: Saved Program Count

### Problem

Users needed quick feedback after saving programs.

### Solution

Added a saved program count in the navigation bar.

Example:

```text
Saved (2)
```

### Implementation

- Updated `base.html`
- Used `request.session.bookmarked_programs`
- Displayed the saved count beside the Saved link

### Alignment

- Reuses bookmark session data
- No new model or database change was needed
- Gives users clear feedback

---

## Improvement 6: Program Link Sharing

### Problem

Users may want to send a useful program to another person, such as a family member, support worker, or community staff member.

### Solution

Added a Share Program button to each program card. If browser sharing is supported, it opens the share option. If not, it copies the program link.

### Implementation

- Updated `programs.html`
- Added `shareProgram()` JavaScript function
- Used browser share and clipboard features

### Alignment

- No external library was added
- Uses simple browser features
- Makes program information easier to share

---

## Files Changed or Added

```text
youthjustice_app/
├── models.py
├── admin.py
├── forms.py
├── views.py
├── urls.py
├── templates/
│   └── youthjustice_app/
│       ├── base.html
│       ├── programs.html
│       ├── requests.html
│       ├── compare_programs.html
│       └── bookmarks.html
└── migrations/
    └── 0007_helprequest_programinforeport.py
```

---

## New Routes Added

| Route | Purpose |
|------|---------|
| `/requests/` | Submit help requests, report incorrect info, and track request status |
| `/compare/` | Compare selected programs |
| `/bookmarks/` | View saved programs |
| `/programs/<pk>/bookmark/` | Save a program |
| `/programs/<pk>/remove-bookmark/` | Remove a saved program |

---

## Consequences

### Positive

- Users can interact with the program directory more meaningfully
- Users can request help and track request status
- Incorrect program information can be reported
- Programs can be compared side by side
- Useful programs can be saved for later
- Program links can be shared easily
- No unnecessary external dependencies were added

### Negative

- Bookmarks are stored in the browser session, so they are not permanent across devices
- Request tracking is simple and not connected to a full user account dashboard
- The share feature depends on browser support, but it still copies the link as a fallback

---

## Team Contribution

- **Nawshin Nawar Tanisha:** Implemented user request and report functionality, request status tracking, program comparison, bookmark functionality, saved count in navigation, program link sharing, related templates, routes, view logic, and this ADR.

---

## Alignment with Other ADRs

- **Quick Development:** Uses Django’s built-in forms, views, templates, URLs, sessions, and admin support
- **Less Code:** Avoids unnecessary external libraries and complex systems
- **Separate Logic from Presentation:** Views handle logic, templates display the result
- **Data Encapsulation:** Request and report data are stored in proper models
- **Functionality Improvements:** Focuses on real user actions, not only visual changes