\# ADR: User Interaction Features Improvements - Assessment 4



\## Status

Accepted



\---



\## Context



After completing the initial build of the Youth Justice NT application, the system already had several useful features, including a program directory with search and filtering, dashboards, organisation pages, CSV exports, and authenticated program management. However, the program directory still worked mostly as an information display system.



Users could browse programs, but they had limited ways to interact with the program information. For a real-world youth support directory, users may need to request help, report incorrect information, compare programs, save useful programs, or share program links with someone else.



The teaching team specifically requested \*\*better functionality over better visuals\*\*. This ADR documents the user interaction functionality improvements implemented for Assessment 4 and explains how they make the system more useful for public users, families, support workers, and community staff.



\---



\## Decision



I implemented \*\*6 targeted user interaction functionality improvements\*\* across the program directory. These improvements focus on practical user actions rather than only improving the visual design.



The improvements include:



1\. User request and report functionality

2\. Request status tracking

3\. Program comparison

4\. Program bookmark functionality

5\. Saved program count in the navigation bar

6\. Program link sharing



These features were implemented using Django’s existing structure, including models, forms, views, URLs, templates, sessions, Django admin, and simple JavaScript. No unnecessary external dependencies were added.



\---



\## Improvement 1: User Request and Report Page



\### Problem



The application allowed users to browse youth support programs, but there was no simple way for users to ask for help or send a question about a program. This made the directory feel more like a static information page rather than an interactive support tool.



There was also no way for users to report incorrect or outdated program information, such as a broken website link, wrong contact information, or wrong availability status.



\### Solution



Added a new `/requests/` page where users can submit a help request about a selected program. The request stores the user’s name, email, selected program, message, and request status.



The same page also allows users to report incorrect or outdated program information. These reports can later be reviewed by staff through the Django admin panel.



\### Implementation



\- \*\*Models:\*\* Added `HelpRequest` and `ProgramInfoReport`

\- \*\*Forms:\*\* Added `HelpRequestForm` and `ProgramInfoReportForm`

\- \*\*Views:\*\* Added `requests\_page`

\- \*\*Templates:\*\* Added `requests.html`

\- \*\*URLs:\*\* Added `/requests/`

\- \*\*Admin:\*\* Registered help requests and program info reports so staff can review them



\### Alignment



\- \*\*Separate Logic from Presentation (ADR3):\*\* Form handling is done in views and forms, while the template only displays the page.

\- \*\*Data Encapsulation ADR:\*\* Request and report data are stored in proper Django models.

\- \*\*Quick Development (ADR1):\*\* Uses Django ModelForms and normal view handling instead of creating a complex custom system.



\---



\## Improvement 2: Request Status Tracking



\### Problem



If users submit a help request, they need some way to check what happened after submission. Without tracking, the request form would feel incomplete because users would not know whether their request was new, reviewed, contacted, or closed.



\### Solution



Added simple request status tracking using a request ID and email address. Users can enter these details on the Requests page and see the current status of their help request.



This keeps the feature simple while still giving users a clear follow-up option.



\### Implementation



\- \*\*Model field:\*\* Added `status` to the `HelpRequest` model

\- \*\*View logic:\*\* The `requests\_page` checks request ID and email

\- \*\*Template:\*\* Shows request status, program name, message, and submitted date

\- \*\*Admin:\*\* Staff can update request status from Django admin



\### Alignment



\- \*\*Less Code (ADR2):\*\* Uses the existing request model instead of adding a separate tracking system.

\- \*\*Quick Development (ADR1):\*\* Simple ID and email lookup keeps the feature easy to test and explain.

\- \*\*Separate Logic from Presentation (ADR3):\*\* Status lookup is handled in the view, while the template only shows the result.



\---



\## Improvement 3: Program Comparison



\### Problem



Users could browse and filter programs, but they could not easily compare programs side by side. This makes decision-making harder, especially when programs have similar names, regions, categories, or age ranges.



For example, a user may want to compare two mentoring programs or two diversion programs before choosing which one may be more suitable.



\### Solution



Added a program comparison page where users can compare two or three programs. The comparison shows key program details such as organisation, region, category, age range, availability, description, and website.



A “Compare This Program” link was also added to each program card, so users can start comparison directly from the Programs page.



\### Implementation



\- \*\*Views:\*\* Added `compare\_programs`

\- \*\*Templates:\*\* Added `compare\_programs.html`

\- \*\*Programs page:\*\* Added “Compare This Program” action to each program card

\- \*\*URLs:\*\* Added `/compare/`

\- \*\*Query parameters:\*\* Used `program\_1`, `program\_2`, and `program\_3` to keep selected programs



\### Alignment



\- \*\*Less Code (ADR2):\*\* Uses existing `Program` data without creating a new model.

\- \*\*Data Encapsulation ADR:\*\* Uses existing program properties such as `age\_range\_display`.

\- \*\*Quick Development (ADR1):\*\* Uses simple GET parameters and Django templates.



\---



\## Improvement 4: Program Bookmark Functionality



\### Problem



Users may find useful programs while browsing, but there was no way to save them for later. This means users would have to search again every time they wanted to return to a program.



This is not ideal for users who may be comparing multiple support options or looking through several programs before making a decision.



\### Solution



Added bookmark functionality so users can save programs while browsing and view them later from the Saved page. Users can also remove saved programs when they no longer need them.



The bookmark feature uses browser session data, which keeps the implementation simple and avoids adding unnecessary database tables.



\### Implementation



\- \*\*Views:\*\* Added `add\_bookmark`, `remove\_bookmark`, and `bookmarks\_page`

\- \*\*Templates:\*\* Added `bookmarks.html`

\- \*\*Program pages:\*\* Added save and remove bookmark actions

\- \*\*URLs:\*\* Added bookmark routes

\- \*\*Session data:\*\* Saved program IDs in `request.session`



\### Alignment



\- \*\*Less Code (ADR2):\*\* Uses Django sessions instead of creating a new bookmark model.

\- \*\*Quick Development (ADR1):\*\* Session-based saving is simple and works well for this student project.

\- \*\*Separate Logic from Presentation (ADR3):\*\* Bookmark logic is handled in views, while templates display saved programs.



\---



\## Improvement 5: Saved Program Count in Navbar



\### Problem



Users could save programs, but they needed quick feedback to know how many programs were saved. Without a count, the bookmark feature felt less visible and users might not realise their saved list had updated.



\### Solution



Added a saved program count to the navigation bar. The navbar shows the number of saved programs from the current browser session.



Example:



```text

Saved (2)

```



This gives users quick feedback after saving or removing programs.



\### Implementation



\- \*\*Template:\*\* Updated `base.html`

\- \*\*Session:\*\* Used `request.session.bookmarked\_programs` to show the saved count

\- \*\*Navigation:\*\* Added the saved count beside the Saved link



\### Alignment



\- \*\*Less Code (ADR2):\*\* Uses the same session data from the bookmark feature.

\- \*\*Quick Development (ADR1):\*\* Simple template update with no extra model or database change.

\- \*\*Functionality focus:\*\* Gives users clear feedback about saved programs.



\---



\## Improvement 6: Share Program Link



\### Problem



Users may want to send a useful program to someone else, such as a family member, support worker, or community staff member. Previously, users had to manually copy the page link themselves.



This is not very user-friendly, especially for people who quickly want to share a program with someone who may need support.



\### Solution



Added a Share Program button to each program card. If the browser supports native sharing, the button opens the browser share option. If not, the program link is copied to the clipboard.



This makes sharing program information easier and more realistic for the type of users the system is designed for.



\### Implementation



\- \*\*Template:\*\* Updated `programs.html`

\- \*\*JavaScript:\*\* Added `shareProgram()` function

\- \*\*Fallback:\*\* If `navigator.share` is not available, the link is copied using `navigator.clipboard`

\- \*\*Program cards:\*\* Added Share Program button beside other program actions



\### Alignment



\- \*\*Quick Development (ADR1):\*\* Uses built-in browser sharing and clipboard features.

\- \*\*Less Code (ADR2):\*\* No external package or library was added.

\- \*\*Real-world utility:\*\* Makes it easier for users to share youth support information.



\---



\## Files Changed / Added



```text

youthjustice\_app/

├── models.py                                  # MODIFIED - added HelpRequest and ProgramInfoReport

├── admin.py                                   # MODIFIED - registered request and report models

├── forms.py                                   # MODIFIED - added request and report forms

├── views.py                                   # MODIFIED - added request, comparison, and bookmark views

├── urls.py                                    # MODIFIED - added request, compare, and bookmark routes

├── templates/

│   └── youthjustice\_app/

│       ├── base.html                          # MODIFIED - added Requests, Compare, and Saved count links

│       ├── programs.html                      # MODIFIED - added Compare This Program and Share Program actions

│       ├── requests.html                      # NEW - user request, report, and status tracking page

│       ├── compare\_programs.html              # NEW - program comparison page

│       └── bookmarks.html                     # NEW - saved programs page

└── migrations/

&#x20;   └── 0007\_helprequest\_programinforeport.py  # NEW - database tables for requests and reports

```



\---



\## New URL Routes Added



| Route | View | Purpose |

|-------|------|---------|

| `/requests/` | `requests\_page` | Submit help requests, report incorrect info, and track request status |

| `/compare/` | `compare\_programs` | Compare two or three programs side by side |

| `/bookmarks/` | `bookmarks\_page` | View saved programs |

| `/programs/<pk>/bookmark/` | `add\_bookmark` | Save a program |

| `/programs/<pk>/remove-bookmark/` | `remove\_bookmark` | Remove a saved program |



\---



\## Consequences



\### Positive



1\. \*\*More user interaction\*\* - users can do more than only browse programs.

2\. \*\*Better decision-making\*\* - users can compare programs before choosing one.

3\. \*\*Improved information reliability\*\* - users can report outdated or incorrect program details.

4\. \*\*Better follow-up\*\* - users can track the status of help requests.

5\. \*\*More practical browsing\*\* - users can save programs and return to them later.

6\. \*\*Easier sharing\*\* - users can share program links with others.

7\. \*\*No unnecessary dependencies\*\* - features use Django built-ins and simple browser JavaScript.



\### Negative



1\. Bookmark data is stored in the browser session, so it is not permanent across different browsers or devices.

2\. Request tracking is simple and based on request ID and email, not a full user account dashboard.

3\. The share button depends on browser support, although it still copies the link when native sharing is not available.

4\. Adding more user actions makes the Programs page busier, so the layout may need small design improvements later.



\---



\## Team Contribution



\- \*\*Nawshin Nawar Tanisha:\*\* Implemented user request and report functionality, request status tracking, program comparison, bookmark functionality, saved count in navigation, share program link feature, related templates, routes, view logic, and this ADR.



\---



\## Alignment with Other ADRs



\- \*\*ADR: Quick Development\*\* - The improvements use Django’s built-in forms, views, templates, URL routing, sessions, and admin support.

\- \*\*ADR: Less Code\*\* - The features avoid unnecessary external libraries. Bookmarks use sessions, comparison uses existing Program data, and sharing uses browser APIs.

\- \*\*ADR: Separate Logic from Presentation\*\* - Views handle logic, forms handle input, templates handle display.

\- \*\*ADR: Data Encapsulation\*\* - Requests and reports are stored as models, while program-related features use existing program fields and properties.

\- \*\*ADR: Functionality Improvements\*\* - These changes focus on useful user actions rather than only changing the visual design.

