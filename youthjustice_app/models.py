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

