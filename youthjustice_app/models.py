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

