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
    3. Skips rows with missing or invalid count values
    4. Creates CrimeData objects for each valid row
    5. Bulk inserts all records into the database at once

This is idempotent — safe to run multiple times.
"""

import csv
import os
from django.core.management.base import BaseCommand
from youthjustice_app.models import CrimeData


class Command(BaseCommand):
    help = "Import NT Crime Statistics from CSV into the database"

    def handle(self, *args, **options):

        # path to the CSV file (relative to project root)
        file_path = os.path.join("dataset", "nt_crime_statistics_aug_2025.csv")

        # check if file exists
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(
                f"File not found: {file_path}"
            ))
            self.stderr.write(
                "Make sure the CSV file is in the data/ folder."
            )
            return

        # step 1: clear old data
        deleted_count = CrimeData.objects.count()
        CrimeData.objects.all().delete()
        self.stdout.write(f"Cleared {deleted_count} old crime records.")

        # step 2: read CSV and build records
        records = []
        skipped = 0

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # get the count value, skip if empty or not a number
                raw_count = row.get("Number of offences", "").strip()
                if not raw_count or raw_count == "" or raw_count == "-":
                    skipped += 1
                    continue

                try:
                    count = int(raw_count)
                except ValueError:
                    skipped += 1
                    continue

                # get year and month
                try:
                    year = int(row.get("Year", "0"))
                    month = int(row.get("Month number", "0"))
                except ValueError:
                    skipped += 1
                    continue

                # skip if year or month is invalid
                if year == 0 or month == 0:
                    skipped += 1
                    continue

                # create the record object (not saved yet)
                record = CrimeData(
                    year=year,
                    month=month,
                    offence_category=row.get("Offence category", "").strip(),
                    offence_type=row.get("Offence type ", "").strip(),  # note: trailing space in CSV header
                    alcohol_involvement=row.get("Alcohol involvement", "-").strip(),
                    dv_involvement=row.get("DV involvement", "-").strip(),
                    region=row.get("Reporting Region", "").strip(),
                    count=count,
                )
                records.append(record)

        # step 3: bulk insert all records at once (much faster)
        CrimeData.objects.bulk_create(records)

        # step 4: print summary
        self.stdout.write(self.style.SUCCESS(
            f"Successfully imported {len(records)} crime records."
        ))
        if skipped > 0:
            self.stdout.write(f"Skipped {skipped} rows (empty/invalid data).")
