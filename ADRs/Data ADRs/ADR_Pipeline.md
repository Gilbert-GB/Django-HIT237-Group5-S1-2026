# ADR: Data Import Pipeline Design

## Status
Accepted

---

## Context
The Youth Justice NT application needs to display statistical data from two external government sources:

1. **NT Crime Statistics** — 6,574 records of monthly offence data across 7 NT regions (Darwin, Alice Springs, Katherine, Palmerston, Tennant Creek, Nhulunbuy, NT Balance), covering 9 offence categories from Dec 2023 to Aug 2025.

2. **Closing the Gap Target 7** — 370 valid records of youth engagement rates (employment, education, or training) for Indigenous and non-Indigenous people aged 15–24 in the NT, from ABS Census data (2006–2021).

The challenge is: how do we get this external CSV data into our Django database so that views can query it and templates can display it? The data is not entered by users — it comes from downloaded government files.

---

## Decision
We will use **Django custom management commands** to import the CSV files into two new database models (`CrimeData` and `EngagementData`). The commands are run from the terminal and handle the entire pipeline: reading, cleaning, and inserting data.

### How It Works

**Step 1:** Place CSV files in a `data/` folder inside the project root.

**Step 2:** Run the import commands:
```
python manage.py import_crime_data
python manage.py import_ctg_data
```

**Step 3:** The commands:
- Delete all existing records for that dataset (clean slate)
- Read the CSV file using Python's built-in `csv` module
- Skip invalid rows (missing values, empty counts, projection data)
- Create model instances for each valid row
- Use `bulk_create()` to insert all records in one database operation

**Step 4:** Data is now in SQLite and can be queried by views using Django ORM.

---

## New Models Added

### CrimeData
| Field | Type | Source Column |
|-------|------|---------------|
| year | IntegerField | Year |
| month | IntegerField | Month number |
| offence_category | CharField | Offence category |
| offence_type | CharField | Offence type |
| alcohol_involvement | CharField | Alcohol involvement |
| dv_involvement | CharField | DV involvement |
| region | CharField | Reporting Region |
| count | IntegerField | Number of offences |

### EngagementData
| Field | Type | Source Column |
|-------|------|---------------|
| year | IntegerField | Year |
| sex | CharField | Sex |
| indigenous_status | CharField | Indigenous_Status |
| measure | CharField | Measure |
| value_nt | FloatField | NT |
| value_national | FloatField | Aust |

---

## Alternatives Considered

### 1. Read CSV files directly in views every time a page loads
**Pros:** No new models needed.
**Cons:** Extremely slow — the crime CSV has 6,574 rows. Reading and parsing it on every page request would make the site unusable. Cannot use Django ORM filtering, sorting, or aggregation.

### 2. Import full datasets with all columns into one large model
**Pros:** Retains every column from the source file.
**Cons:** Many columns are not needed (e.g., `As At`, `Statistical Area 2`). Wastes storage. Makes queries more complex. Not aligned with ADR1's "simplify and store relevant data" principle.

### 3. Use Django custom management commands with simplified models (Chosen)
**Pros:**
- Fast — `bulk_create()` inserts thousands of records in seconds
- Idempotent — safe to re-run; deletes old data before re-importing
- Uses Django ORM — views can filter, aggregate, and sort using familiar Python syntax
- Clean separation — data loading logic is in management commands, not in views
- Follows the "Less Code" philosophy (ADR2) — uses Python's built-in `csv` module, no extra libraries needed

**Cons:**
- Requires running a terminal command after placing the CSV file
- Some raw columns are not retained (intentional — only relevant fields are kept)

---

## Rationale

This approach aligns with the team's existing ADRs:

- **ADR1 (Quick Development):** Management commands are a built-in Django feature. No extra libraries, no complex setup. One command loads all data.
- **ADR2 (Less Code):** Each import command is under 100 lines. Uses Python's `csv` module (built-in) and Django's `bulk_create()` — no pandas, no external dependencies.
- **ADR3 (Separate Logic from Presentation):** Data loading is completely separate from views and templates. The pipeline runs independently — views just query the models.

### Data Integrity Notes
- **NT Crime Statistics:** The metadata warns about a recording system change after Nov 2023. All our data is from Dec 2023 onward, so it is internally consistent.
- **Closing the Gap:** We filter out trajectory/projection rows and only import actual census/survey data. This ensures the displayed values are real measurements, not estimates.

---

## Files Changed / Added

```
youthjustice_app/
├── models.py                              # MODIFIED — added CrimeData, EngagementData
├── admin.py                               # MODIFIED — registered new models
├── management/
│   └── commands/
│       ├── import_crime_data.py           # NEW — imports NT crime CSV
│       └── import_ctg_data.py             # NEW — imports Closing the Gap CSV

data/
├── nt_crime_statistics_aug_2025.csv       # Source file (not committed to Git)
├── ctg-2023-ctg07-employment-education-dataset.csv  # Source file
```

---

## Import Results (Tested)

| Dataset | Valid Records | Skipped Rows | Reason for Skipping |
|---------|--------------|--------------|---------------------|
| NT Crime Statistics | 6,574 | 0 | — |
| Closing the Gap | 370 | 34 | Trajectory/projection rows and missing NT values |

---

**This ADR can be updated as the project development progresses.**
