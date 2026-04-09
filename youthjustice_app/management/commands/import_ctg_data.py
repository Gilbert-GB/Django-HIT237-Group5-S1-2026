"""
Management command: import_ctg_data
Loads Closing the Gap Target 7 (youth engagement) data into EngagementData model.

Usage:
    python manage.py import_ctg_data

The CSV file must be placed at:
    data/ctg-2023-ctg07-employment-education-dataset.csv

What this command does:
    1. Deletes all existing EngagementData records (clean reload)
    2. Reads the CSV file
    3. Filters for actual census data only (skips trajectory/projection rows)
    4. Extracts NT and National (Aust) values
    5. Skips rows where NT value is missing (..)
    6. Bulk inserts all valid records

This is idempotent — safe to run multiple times.
"""

import csv
import os
from django.core.management.base import BaseCommand
from youthjustice_app.models import EngagementData


class Command(BaseCommand):
    help = "Import Closing the Gap youth engagement data from CSV"

    def handle(self, *args, **options):

        # path to the CSV file
        file_path = os.path.join(
            "dataset",
            "ctg-2023-ctg07-employment-education-dataset.csv"
        )

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
        deleted_count = EngagementData.objects.count()
        EngagementData.objects.all().delete()
        self.stdout.write(f"Cleared {deleted_count} old engagement records.")

        # step 2: read CSV and build records
        records = []
        skipped = 0

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # skip trajectory and projection rows
                # we only want actual census/survey data
                description2 = row.get("Description2", "").strip()
                if description2 in ["Trajectory", "Linear regression estimates"]:
                    skipped += 1
                    continue

                # get NT value — skip if missing (..)
                nt_raw = row.get("NT", "").strip()
                if nt_raw == ".." or nt_raw == "" or nt_raw == "np":
                    skipped += 1
                    continue

                # try to convert NT value to float
                try:
                    value_nt = float(nt_raw)
                except ValueError:
                    skipped += 1
                    continue

                # get national (Aust) value
                aust_raw = row.get("Aust", "").strip()
                value_national = None
                if aust_raw and aust_raw != ".." and aust_raw != "np":
                    try:
                        value_national = float(aust_raw)
                    except ValueError:
                        value_national = None

                # get year
                try:
                    year = int(row.get("Year", "0"))
                except ValueError:
                    skipped += 1
                    continue

                if year == 0:
                    skipped += 1
                    continue

                # create record
                record = EngagementData(
                    year=year,
                    sex=row.get("Sex", "").strip(),
                    indigenous_status=row.get("Indigenous_Status", "").strip(),
                    measure=row.get("Measure", "").strip(),
                    value_nt=value_nt,
                    value_national=value_national,
                )
                records.append(record)

        # step 3: bulk insert
        EngagementData.objects.bulk_create(records)

        # step 4: print summary
        self.stdout.write(self.style.SUCCESS(
            f"Successfully imported {len(records)} engagement records."
        ))
        if skipped > 0:
            self.stdout.write(f"Skipped {skipped} rows (projections/missing NT data).")
