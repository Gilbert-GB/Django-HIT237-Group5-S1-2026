# Architecture Decision Record (ADR)
## Using Django QuerySet APIs for Data Processing

## Status
Accepted

## Last updated
2026-05-26

---

## Introduction

### Prologue (Summary)
As part of developing the data analytics component of the Youth Justice NT application, we needed an efficient way to process and analyse large volumes of crime data. Instead of writing raw SQL queries, we adopted Django’s QuerySet API to follow the design philosophy of **less code and higher abstraction**.

This approach allows us to perform complex data aggregation (such as trends, totals, and rankings) directly within Django, improving development speed, readability, and maintainability while slightly reducing low-level control.

---

## Discussion (Context)

The project requires handling structured datasets such as crime statistics and engagement data. These datasets need to be transformed into meaningful insights for the dashboard, including:

- Monthly crime trends  
- Top regions with highest crime rates  
- Crime category breakdowns  
- Key performance indicators (KPIs)  

Writing raw SQL for these operations would:
- Increase code complexity  
- Make debugging harder  
- Reduce readability for beginner-level developers  

Django provides a built-in ORM (Object Relational Mapper) with QuerySet APIs that simplify these operations through Python-based queries.

---

## Solution (Decision)

We decided to use Django QuerySet APIs for all data processing tasks instead of raw SQL.

Key implementations include:

- Using `.values()` to group data  
- Using `.annotate()` with aggregation functions (e.g. `Sum`)  
- Using `.aggregate()` for overall metrics  
- Using `.order_by()` to rank results  

### Example

```python
CrimeData.objects.values("region") \
    .annotate(total=Sum("count")) \
    .order_by("-total")
```