# Group Contract – Group 5

## Project Theme

Our project focuses on youth justice in the Northern Territory by developing a platform that provides a searchable directory of youth diversion and support programs. The system will use public datasets such as NT Crime Statistics, AIHW Youth Justice data, Closing the Gap, and ABS Recorded Crime to support awareness and decision-making.

## We are aiming for at least Distinction for this unit.

## Section 1: Terms and Conditions of Group Work

### Group Allocation

Grades will be awarded equally to all members, assuming each member contributes fairly. Roles will be assigned based on individual strengths and skills (e.g., development, design, data, documentation, managing Django). A fair contribution includes completing assigned tasks on time, actively participating in discussions, and supporting team progress.

### Communication

Microsoft Teams is our group`s official communication channel. All team members are understood to have mutually agreed to meet twice a week, once for an online meeting (scheduling dependent on progress) and a regular in-person meeting on Tuesdays after class. Acceptable response timings would be 24 hours at maximum while serious situations such as Health or Family issues can be considered as exceptions. Meeting minutes shall be updated after each meeting and the videos would be recorded and stored in Microsoft Teams.

### Task Ownership

Tasks will be assigned during team meetings and can also be tracked through Microsoft Teams. Each member is responsible for updating their progress in meeting minutes. If a member is unable to complete a task or falls behind, they must inform the group early (at least a week before the due date). The team may reassign tasks if needed to ensure deadlines are met.

### Diverse Working Styles

We recognise that team members may have different schedules, learning speeds, and personal commitments. The group will allow flexible working arrangements and support each other where needed. Deadlines and expectations will be discussed openly to ensure fairness. Clear communication will be maintained so that all members can contribute effectively regardless of their working style.

### Conflict Resolution

Since all roles allocated in project development are mutually agreed upon, all members are expected to perform their tasks appropriately and on time. In any conflict, members will re-discuss their responsibilities based on this group contract and aim to reach a quick resolution. If unresolved, the teaching team will be consulted.

### Academic Integrity

All team members have reviewed CDU’s academic integrity policies. AI tools may be used for learning, scaffolding, and improving efficiency, but all members must fully understand and test the code they contribute. Any AI-assisted content will be appropriately acknowledged where required.

---

## Section 2: Provisional Milestones and Checkpoints

### Milestones

- Week 2-3: Finalise project idea and requirements
- Week 4: Collect and review data sources (NT crime data, AIHW, ABS)
- Week 5-6: Design system structure and database
- Week 7: Draft and submit Assessment 2
- Week 8-9: Develop features (search, filters, program listings, dashboard)
- Week 10: Draft Assessment 4
- Week 11–12: Testing, improvements, and final submission

---

## Task Breakdown

- **Gilbert (Data & System Integration):**
  - Collect and clean datasets (NT Crime Statistics, AIHW, ABS)
  - Design and implement **Django models and QuerySet APIs**
  - Develop **interactive dashboard (KPIs, charts, trends)**
  - Implement **filters (region, category, year) using QuerySets**
  - Lead **backend integration (views, APIs, JSON responses)**
  - Support frontend integration (Chart.js visualisation)
  - Manage GitHub integration and resolve merge conflicts

- **Ahmad (Architecture, Backend Refactoring & Documentation):**
  - Led **architecture refinement** of the Django app to better align with the rubric and assignment requirements
  - Designed and documented **model relationships**, including adding the `Organisation` model and linking it to `Program`
  - Reworked the **backend structure** using existing team logic, reorganising the app into a cleaner and more maintainable design
  - Implemented and finalised **CRUD functionality** for programs in views and templates
  - Created and updated **forms** for program data handling
  - Designed and implemented **custom managers**, including moving managers into a separate file for cleaner separation of concerns
  - Improved **URL and view structure** to support clearer public pages and management pages
  - Finalised **template structure and shared frontend layout** for consistent app design
  - Wrote and refined major **Architectural Decision Records (ADRs)**, including:
    - model relationships
    - CRUD design
    - separate managers
    - Django design philosophies
  - Created supporting **ERDs, class diagrams, and architecture diagrams**
  - Reviewed the project against the **assessment rubric** and identified missing areas for improvement
  - Helped rebuild the app backend in a cleaner structure suitable for viva explanation and final submission

- **All Members:**
  - Research youth justice policies and community programs
  - Contribute to testing and feedback
  - Finalsed project submission after reviewing final draft

- **Mahathir:**
  - System design (architecture, database structure)
  - Documentation writing (reports, ADRs)

- **Nawshin:**
  - **Django model development** (Program and Organisation structure)
  - **Frontend implementation** (home, programs, about, and detail pages)
  - **Template design and UI improvements** (layout, styling, consistency)
  - **Integration of backend data with frontend templates**
  - **Final review**
  - **Quality checking** (formatting, consistency, completeness)

---

## Checkpoints

- Weekly meetings to review progress
- Data review checkpoint (Week 4)
- Draft review before Assessment 2
- Final review before Assessment 4 submission

---

## Integration

All work will be uploaded to GitHub and merged regularly. Gilbert will lead integration of backend and dashboard features, while all members are responsible for reviewing and approving changes before submission.

---

## Data Sources (Gilbert)

- NT Crime Statistics (monthly data by offence and location)
- AIHW Youth Justice in Australia reports (NT-specific data)
- Closing the Gap dashboard (youth engagement data)
- ABS Recorded Crime — Offenders data

---

## Agreement

By contributing to this document, all members agree to follow the terms above.

- Member 1: Mahathir Md Taief
- Member 2: Gilbertofer Tanoto
- Member 3: Nawshin Nawar Tanisha
- Member 4: Muhammad Ahmad
