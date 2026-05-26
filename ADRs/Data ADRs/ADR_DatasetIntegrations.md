# ADR: Integration and Storage of External Data Sources

## Status  
Accepted

## Last updated
2026-05-26

---

## Context  
The application requires the use of multiple external data sources, including:

- NT Crime Statistics (CSV)  
- AIHW Youth Justice data (XLSX)  
- Closing the Gap dashboard  
- ABS Recorded Crime data  

These datasets are large, complex, and designed for reporting rather than direct application use. The system needs to present meaningful insights through a dashboard while maintaining performance and simplicity.

---

## Decision  
We will **select, simplify, and store relevant data from external datasets into Django models**, instead of using raw files directly.

Only key attributes (e.g., offence type, location, time, summary values) will be extracted and transformed into structured database models to support efficient querying and dashboard visualisation.

---

## Alternatives Considered  

### 1. Use raw CSV/XLSX files directly  
**Pros:**
- Simple setup  
- No database required  

**Cons:**
- Inefficient for repeated queries  
- Difficult to integrate with Django features  
- Poor scalability  

---

### 2. Import full datasets without modification  
**Pros:**
- Retains complete data  

**Cons:**
- Unnecessary complexity  
- Harder to manage and query  
- Not aligned with system needs  

---

### 3. Store simplified data in Django models (Chosen)  
**Pros:**
- Efficient querying using Django ORM  
- Supports dashboard features  
- Improves performance and maintainability  

**Cons:**
- Requires preprocessing  
- Some raw data is not retained  

---

## Rationale  
This approach ensures the system remains efficient and focused on user needs. It aligns with key design philosophies:
 

---

## Code References  

```text
data/models.py  
data/management/commands/  
```