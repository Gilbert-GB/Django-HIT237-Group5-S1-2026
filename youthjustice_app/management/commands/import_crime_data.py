"""
Management command: import_crime_data
Loads NT Crime Statistics CSV into the CrimeData model.

Usage:
    python manage.py import_crime_data

The CSV file must be placed at:
    dataset/nt_crime_statistics_aug_2025.csv

What this command does:
    1. Deletes all existing CrimeData records (clean reload)
    2. Reads the CSV file row by row
    3. Skips rows with missing or invalid values
    4. Cleans and converts data types
    5. Bulk inserts all records into the database

This is idempotent — safe to run multiple times.
"""

import csv
import os
from django.core.management.base import BaseCommand
from youthjustice_app.models import CrimeData


class Command(BaseCommand):
    help = "Import NT Crime Statistics from CSV into the database"

    def handle(self, *args, **options):

        # File path (relative to project root)
        file_path = os.path.join("dataset", "nt_crime_statistics_aug_2025.csv")

        # Check if file exists
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(
                f"File not found: {file_path}"
            ))
            self.stderr.write(
                "Make sure the CSV file is in the dataset/ folder."
            )
            return

        # Step 1: Clear old data (clean reload approach)
        deleted_count = CrimeData.objects.count()
        CrimeData.objects.all().delete()
        self.stdout.write(f"Cleared {deleted_count} old crime records.")

        # Step 2: Read CSV and process data
        records = []
        skipped = 0

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    # Clean and validate count
                    raw_count = row.get("Number of offences", "").strip()
                    if not raw_count or raw_count == "-":
                        skipped += 1
                        continue

                    count = int(raw_count)

                    # Clean and validate year & month
                    year = int(row.get("Year", "0"))
                    month = int(row.get("Month number", "0"))

                    if year == 0 or month == 0:
                        skipped += 1
                        continue

                    # Handle possible header inconsistency (trailing space issue)
                    offence_type = (
                        row.get("Offence type", "").strip()
                        or row.get("Offence type ", "").strip()
                    )

                    # Create object (not saved yet)
                    record = CrimeData(
                        year=year,
                        month=month,
                        offence_category=row.get("Offence category", "").strip(),
                        offence_type=offence_type,
                        alcohol_involvement=row.get("Alcohol involvement", "-").strip(),
                        dv_involvement=row.get("DV involvement", "-").strip(),
                        region=row.get("Reporting Region", "").strip(),
                        count=count,
                    )

                    records.append(record)

                except Exception:
                    skipped += 1
                    continue

        # Step 3: Bulk insert (fast and efficient)
        CrimeData.objects.bulk_create(records, batch_size=1000)

        # Step 4: Output results
        self.stdout.write(self.style.SUCCESS(
            f"Successfully imported {len(records)} crime records."
        ))

        if skipped > 0:
            self.stdout.write(f"Skipped {skipped} rows (invalid or missing data).")