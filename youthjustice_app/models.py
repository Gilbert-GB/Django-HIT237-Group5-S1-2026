from django.db import models

# Models are being created here
class Program(models.Model):

    # predefined categories for dropdown selection
    CATEGORY_CHOICES = [
        ("diversion", "Diversion"),
        ("throughcare", "Throughcare"),
        ("support", "Support"),
        ("mentoring", "Mentoring"),
        ("justice", "Justice"),
        ("education", "Education"),
        ("rehabilitation", "Rehabilitation"),
        ("other", "Other"),
    ]

    # NT regions for filtering programs
    REGION_CHOICES = [
        ("darwin", "Darwin"),
        ("alice_springs", "Alice Springs"),
        ("katherine", "Katherine"),
        ("tennant_creek", "Tennant Creek"),
        ("nhulunbuy", "Nhulunbuy"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)

    # using choices so it appears as dropdown in admin
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    short_description = models.TextField()

    # optional fields
    website = models.URLField(blank=True, null=True)

    # auto timestamp when record is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =====================================================================
# DATA PIPELINE MODELS (Added by Mahathir)
# These models store external dataset records imported via management
# commands. They are NOT entered manually through admin — they are
# loaded from CSV files using the import commands.
# =====================================================================

class CrimeData(models.Model):
    """
    Stores NT Crime Statistics data.
    Source: NT Department of the Attorney-General and Justice
    File: nt_crime_statistics_aug_2025.csv
    """

    year = models.IntegerField()
    month = models.IntegerField()
    offence_category = models.CharField(max_length=200)
    offence_type = models.CharField(max_length=200)
    alcohol_involvement = models.CharField(max_length=20, default="-")
    dv_involvement = models.CharField(max_length=20, default="-")
    region = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Crime Statistic"
        verbose_name_plural = "Crime Statistics"

    def __str__(self):
        return f"{self.region} - {self.offence_category} ({self.year}/{self.month})"


class EngagementData(models.Model):
    """
    Stores Closing the Gap Target 7 data — youth engagement in
    employment, education or training for NT.
    Source: Productivity Commission / ABS Census
    File: ctg-2023-ctg07-employment-education-dataset.csv
    """

    year = models.IntegerField()
    sex = models.CharField(max_length=30)
    indigenous_status = models.CharField(max_length=100)
    measure = models.CharField(max_length=300)
    value_nt = models.FloatField(null=True, blank=True)
    value_national = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Engagement Record"
        verbose_name_plural = "Engagement Data"

    def __str__(self):
        return f"{self.indigenous_status} - {self.sex} ({self.year})"
