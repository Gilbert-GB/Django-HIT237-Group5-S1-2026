from django.db import models
from django.core.exceptions import ValidationError


# =====================================================================
# PROGRAM MODEL
# =====================================================================

class ProgramManager(models.Manager):
    """
    Custom manager to encapsulate common Program queries.
    Instead of writing filter logic in views, we put it here
    so the model controls how its own data is accessed.
    """

    def available(self):
        """Returns only available programs."""
        return self.filter(is_available=True)

    def featured(self):
        """Returns only featured programs."""
        return self.filter(is_featured=True, is_available=True)

    def by_region(self, region):
        """Returns programs filtered by region."""
        return self.available().filter(region=region)

    def by_category(self, category):
        """Returns programs filtered by category."""
        return self.available().filter(category=category)

    def search(self, query):
        """Search programs by name or organisation (case-insensitive)."""
        return self.available().filter(
            models.Q(name__icontains=query)
            | models.Q(organisation__icontains=query)
            | models.Q(short_description__icontains=query)
        )


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

    # attach custom manager
    objects = ProgramManager()

    # -----------------------------------------------------------------
    # ENCAPSULATION: Validation — model protects its own data
    # -----------------------------------------------------------------
    def clean(self):
        """
        Validates data before saving. Django calls this automatically
        in forms and admin. This ensures no bad data gets into the DB.
        """
        # age_min must be less than age_max
        if self.age_min and self.age_max:
            if self.age_min > self.age_max:
                raise ValidationError(
                    "Minimum age cannot be greater than maximum age."
                )

        # age must be realistic for youth programs (0 to 25)
        if self.age_min is not None and self.age_min < 0:
            raise ValidationError("Minimum age cannot be negative.")

        if self.age_max is not None and self.age_max > 25:
            raise ValidationError(
                "Maximum age should not exceed 25 for youth programs."
            )

        # name should not be empty or just spaces
        if self.name and not self.name.strip():
            raise ValidationError("Program name cannot be blank.")

    def save(self, *args, **kwargs):
        """Override save to run validation automatically."""
        self.full_clean()
        super().save(*args, **kwargs)

    # -----------------------------------------------------------------
    # ENCAPSULATION: Properties — computed values stay inside the model
    # -----------------------------------------------------------------
    @property
    def age_range_display(self):
        """Returns a formatted age range string like '10 - 17 years'."""
        return f"{self.age_min} - {self.age_max} years"

    @property
    def is_youth_only(self):
        """Returns True if the program is strictly for under-18s."""
        return self.age_max <= 17

    @property
    def region_display(self):
        """Returns the human-readable region name."""
        return self.get_region_display()

    @property
    def category_display(self):
        """Returns the human-readable category name."""
        return self.get_category_display()

    # -----------------------------------------------------------------
    # ENCAPSULATION: Helper methods — logic stays in the model
    # -----------------------------------------------------------------
    def mark_unavailable(self):
        """Marks a program as not available."""
        self.is_available = False
        self.is_featured = False  # featured programs must be available
        self.save()

    def mark_available(self):
        """Marks a program as available."""
        self.is_available = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# =====================================================================
# DATA PIPELINE MODELS (Added by Mahathir)
# These models store external dataset records imported via management
# commands. They are NOT entered manually through admin — they are
# loaded from CSV files using the import commands.
# =====================================================================

# -----------------------------------------------------------------
# CRIME DATA MODEL
# -----------------------------------------------------------------

class CrimeDataManager(models.Manager):
    """
    Custom manager to encapsulate common CrimeData queries.
    Views should use these methods instead of writing raw filters.
    """

    def by_region(self, region):
        """Returns crime records for a specific region."""
        return self.filter(region=region)

    def by_year(self, year):
        """Returns crime records for a specific year."""
        return self.filter(year=year)

    def by_offence(self, category):
        """Returns crime records for a specific offence category."""
        return self.filter(offence_category=category)

    def total_by_region(self):
        """Returns total offence count grouped by region."""
        return (
            self.values("region")
            .annotate(total=models.Sum("count"))
            .order_by("-total")
        )

    def total_by_year(self):
        """Returns total offence count grouped by year."""
        return (
            self.values("year")
            .annotate(total=models.Sum("count"))
            .order_by("year")
        )

    def total_by_category(self):
        """Returns total offence count grouped by offence category."""
        return (
            self.values("offence_category")
            .annotate(total=models.Sum("count"))
            .order_by("-total")
        )


class CrimeData(models.Model):
    """
    Stores NT Crime Statistics data.
    Source: NT Department of the Attorney-General and Justice
    File: nt_crime_statistics_aug_2025.csv
    """

    MONTH_NAMES = {
        1: "January", 2: "February", 3: "March",
        4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September",
        10: "October", 11: "November", 12: "December",
    }

    year = models.IntegerField()
    month = models.IntegerField()
    offence_category = models.CharField(max_length=200)
    offence_type = models.CharField(max_length=200)
    alcohol_involvement = models.CharField(max_length=20, default="-")
    dv_involvement = models.CharField(max_length=20, default="-")
    region = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    # attach custom manager
    objects = CrimeDataManager()

    # -----------------------------------------------------------------
    # ENCAPSULATION: Validation
    # -----------------------------------------------------------------
    def clean(self):
        """Validates crime data before saving."""
        if self.year and self.year < 2000:
            raise ValidationError("Year must be 2000 or later.")

        if self.month and (self.month < 1 or self.month > 12):
            raise ValidationError("Month must be between 1 and 12.")

        if self.count is not None and self.count < 0:
            raise ValidationError("Offence count cannot be negative.")

    # -----------------------------------------------------------------
    # ENCAPSULATION: Properties
    # -----------------------------------------------------------------
    @property
    def month_name(self):
        """Returns the month as a readable name like 'January'."""
        return self.MONTH_NAMES.get(self.month, "Unknown")

    @property
    def period_display(self):
        """Returns formatted period like 'January 2024'."""
        return f"{self.month_name} {self.year}"

    @property
    def is_alcohol_related(self):
        """Returns True if alcohol was involved in the offence."""
        return self.alcohol_involvement == "Yes"

    @property
    def is_dv_related(self):
        """Returns True if domestic violence was involved."""
        return self.dv_involvement == "Yes"

    @property
    def offence_category_short(self):
        """
        Returns category without the number prefix.
        Example: '02 Assault' becomes 'Assault'
        """
        parts = self.offence_category.split(" ", 1)
        if len(parts) > 1 and parts[0].isdigit():
            return parts[1]
        return self.offence_category

    class Meta:
        verbose_name = "Crime Statistic"
        verbose_name_plural = "Crime Statistics"
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.region} - {self.offence_category_short} ({self.period_display})"


# -----------------------------------------------------------------
# ENGAGEMENT DATA MODEL
# -----------------------------------------------------------------

class EngagementDataManager(models.Manager):
    """
    Custom manager to encapsulate common EngagementData queries.
    """

    def by_year(self, year):
        """Returns engagement records for a specific year."""
        return self.filter(year=year)

    def indigenous_only(self):
        """Returns only Indigenous engagement data."""
        return self.filter(
            indigenous_status="Aboriginal and Torres Strait Islander people"
        )

    def non_indigenous_only(self):
        """Returns only non-Indigenous engagement data."""
        return self.filter(indigenous_status="Non-Indigenous people")

    def by_sex(self, sex):
        """Returns engagement records for a specific sex."""
        return self.filter(sex=sex)

    def nt_trend(self):
        """
        Returns NT engagement values over time for Indigenous people.
        Useful for building trend charts.
        """
        return (
            self.indigenous_only()
            .filter(sex="All people")
            .values("year", "value_nt")
            .order_by("year")
        )


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

    # attach custom manager
    objects = EngagementDataManager()

    # -----------------------------------------------------------------
    # ENCAPSULATION: Validation
    # -----------------------------------------------------------------
    def clean(self):
        """Validates engagement data before saving."""
        if self.year and self.year < 2000:
            raise ValidationError("Year must be 2000 or later.")

        if self.value_nt is not None and (self.value_nt < 0 or self.value_nt > 100):
            raise ValidationError("NT value must be between 0 and 100 (percentage).")

        if self.value_national is not None and (self.value_national < 0 or self.value_national > 100):
            raise ValidationError("National value must be between 0 and 100 (percentage).")

    # -----------------------------------------------------------------
    # ENCAPSULATION: Properties
    # -----------------------------------------------------------------
    @property
    def nt_display(self):
        """Returns NT value formatted as percentage like '41.0%'."""
        if self.value_nt is not None:
            return f"{self.value_nt:.1f}%"
        return "N/A"

    @property
    def national_display(self):
        """Returns national value formatted as percentage."""
        if self.value_national is not None:
            return f"{self.value_national:.1f}%"
        return "N/A"

    @property
    def gap(self):
        """
        Returns the gap between NT and national values.
        Negative means NT is below the national average.
        """
        if self.value_nt is not None and self.value_national is not None:
            return round(self.value_nt - self.value_national, 1)
        return None

    @property
    def gap_display(self):
        """Returns the gap formatted with + or - sign."""
        g = self.gap
        if g is not None:
            sign = "+" if g >= 0 else ""
            return f"{sign}{g}%"
        return "N/A"

    @property
    def is_below_national(self):
        """Returns True if NT value is below the national average."""
        g = self.gap
        if g is not None:
            return g < 0
        return None

    @property
    def is_indigenous(self):
        """Returns True if this record is for Indigenous people."""
        return self.indigenous_status == "Aboriginal and Torres Strait Islander people"

    class Meta:
        verbose_name = "Engagement Record"
        verbose_name_plural = "Engagement Data"
        ordering = ["-year"]

    def __str__(self):
        return f"{self.indigenous_status} - {self.sex} ({self.year})"
