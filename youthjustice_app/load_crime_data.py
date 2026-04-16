import csv
from django.core.management.base import BaseCommand
from youthjustice_app.models import CrimeData


class Command(BaseCommand):
    help = "Load crime data from CSV file"

    def handle(self, *args, **kwargs):

        file_path = "nt_crime_statistics_aug_2025.csv"

        CrimeData.objects.all().delete()  # optional reset

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            objects = []

            for row in reader:
                objects.append(
                    CrimeData(
                        year=int(row["year"]),
                        month=int(row["month"]),
                        region=row["region"],
                        offence_category=row["offence_category"],
                        offence_type=row["offence_type"],
                        count=int(row["count"]),
                    )
                )

        CrimeData.objects.bulk_create(objects)

        self.stdout.write(self.style.SUCCESS("Crime data loaded successfully!"))