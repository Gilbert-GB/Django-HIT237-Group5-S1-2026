from django.core.exceptions import ValidationError
from django.db import models

from .managers import ProgramManager, CrimeDataManager, EngagementDataManager


# ORGANISATION MODEL

# So we use:
# Organisation (1) -----> (many) Program

class Organisation(models.Model):
    ORG_TYPE_CHOICES = [
        ("government", "Government"),
        ("nonprofit", "Non-profit"),
        ("community", "Community"),
        ("education", "Education"),
        ("other", "Other"),
    ]

    # Main organisation name
    name = models.CharField(max_length=200, unique=True)

    organisation_type = models.CharField(
        max_length=20,
        choices=ORG_TYPE_CHOICES,
        default="community",
    )

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True, null=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def clean(self):
        """
        Model-level validation.
        Keeps invalid organisation data out of the DB.
        """
        if self.name and not self.name.strip():
            raise ValidationError("Organisation name cannot be blank.")

    def __str__(self):
        return self.name


# PROGRAM MODEL

# Each Program belongs to one Organisation.

class Program(models.Model):
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

    REGION_CHOICES = [
        ("darwin", "Darwin"),
        ("alice_springs", "Alice Springs"),
        ("katherine", "Katherine"),
        ("tennant_creek", "Tennant Creek"),
        ("nhulunbuy", "Nhulunbuy"),
        ("other", "Other"),
    ]

    # Program title
    name = models.CharField(max_length=200)

    # Relationship:
    # many programs can belong to one organisation
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="programs",
    )

    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    short_description = models.TextField()

    # Optional external website
    website = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Attach custom manager from managers.py
    objects = ProgramManager()

    class Meta:
        ordering = ["name"]
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def clean(self):
        """
        Validation belongs in the model because the model should
        protect its own data.
        """
        
        if self.age_min is not None and self.age_min < 0:
            raise ValidationError("Minimum age cannot be negative.")

        if self.age_max is not None and self.age_max > 25:
            raise ValidationError("Maximum age should not exceed 25 for youth programs.")

        if self.age_min is not None and self.age_max is not None:
            if self.age_min > self.age_max:
                raise ValidationError("Minimum age cannot be greater than maximum age.")

        if self.name and not self.name.strip():
            raise ValidationError("Program name cannot be blank.")

        if self.is_featured and not self.is_available:
            raise ValidationError("A featured program must also be available.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def age_range_display(self):
        return f"{self.age_min} - {self.age_max} years"

    @property
    def is_youth_only(self):
        return self.age_max <= 17

    @property
    def region_display(self):
        return self.get_region_display()

    @property
    def category_display(self):
        return self.get_category_display()

    def mark_unavailable(self):
        self.is_available = False
        self.is_featured = False
        self.save()

    def mark_available(self):
        self.is_available = True
        self.save()

    def __str__(self):
        return self.name


# CRIME DATA SNAPSHOT MODEL

# Relationship:
# Program (1) -----> (many) CrimeDataSnapshot

# related to a program, region, and year.

class CrimeDataSnapshot(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="crime_snapshots",
    )

    year = models.IntegerField()
    region = models.CharField(max_length=100)
    summary = models.TextField()
    total_offences = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "program__name"]

    def clean(self):
        if self.year < 2000:
            raise ValidationError("Year must be 2000 or later.")
        if self.total_offences < 0:
            raise ValidationError("Total offences cannot be negative.")

    def __str__(self):
        return f"{self.program.name} - {self.region} ({self.year})"


# CRIME DATA MODEL

class CrimeData(models.Model):
    MONTH_NAMES = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    year = models.IntegerField()
    month = models.IntegerField()
    offence_category = models.CharField(max_length=200)
    offence_type = models.CharField(max_length=200)
    alcohol_involvement = models.CharField(max_length=20, default="-")
    dv_involvement = models.CharField(max_length=20, default="-")
    region = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    objects = CrimeDataManager()

    class Meta:
        verbose_name = "Crime Statistic"
        verbose_name_plural = "Crime Statistics"
        ordering = ["-year", "-month"]

    def clean(self):
        if self.year and self.year < 2000:
            raise ValidationError("Year must be 2000 or later.")
        if self.month and (self.month < 1 or self.month > 12):
            raise ValidationError("Month must be between 1 and 12.")
        if self.count is not None and self.count < 0:
            raise ValidationError("Offence count cannot be negative.")

    @property
    def month_name(self):
        return self.MONTH_NAMES.get(self.month, "Unknown")

    @property
    def period_display(self):
        return f"{self.month_name} {self.year}"

    @property
    def is_alcohol_related(self):
        return self.alcohol_involvement == "Yes"

    @property
    def is_dv_related(self):
        return self.dv_involvement == "Yes"

    @property
    def offence_category_short(self):
        parts = self.offence_category.split(" ", 1)
        if len(parts) > 1 and parts[0].isdigit():
            return parts[1]
        return self.offence_category

    def __str__(self):
        return f"{self.region} - {self.offence_category_short} ({self.period_display})"


# ENGAGEMENT DATA MODEL

# Imported from CSV and used mainly for dashboard analysis.

class EngagementData(models.Model):
    year = models.IntegerField()
    sex = models.CharField(max_length=30)
    indigenous_status = models.CharField(max_length=100)
    measure = models.CharField(max_length=300)
    value_nt = models.FloatField(null=True, blank=True)
    value_national = models.FloatField(null=True, blank=True)

    objects = EngagementDataManager()

    class Meta:
        verbose_name = "Engagement Record"
        verbose_name_plural = "Engagement Data"
        ordering = ["-year"]

    def clean(self):
        if self.year and self.year < 2000:
            raise ValidationError("Year must be 2000 or later.")
        if self.value_nt is not None and (self.value_nt < 0 or self.value_nt > 100):
            raise ValidationError("NT value must be between 0 and 100.")
        if self.value_national is not None and (
            self.value_national < 0 or self.value_national > 100
        ):
            raise ValidationError("National value must be between 0 and 100.")

    @property
    def nt_display(self):
        if self.value_nt is not None:
            return f"{self.value_nt:.1f}%"
        return "N/A"

    @property
    def national_display(self):
        if self.value_national is not None:
            return f"{self.value_national:.1f}%"
        return "N/A"

    @property
    def gap(self):
        if self.value_nt is not None and self.value_national is not None:
            return round(self.value_nt - self.value_national, 1)
        return None

    @property
    def gap_display(self):
        g = self.gap
        if g is not None:
            sign = "+" if g >= 0 else ""
            return f"{sign}{g}%"
        return "N/A"

    @property
    def is_below_national(self):
        g = self.gap
        if g is not None:
            return g < 0
        return None

    def __str__(self):
        return f"{self.indigenous_status} - {self.sex} ({self.year})"