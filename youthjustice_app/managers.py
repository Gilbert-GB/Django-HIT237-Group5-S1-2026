from django.db import models
from django.db.models import Q, Sum


# PROGRAM MANAGER

# This manager keeps common query logic outside the views.

class ProgramManager(models.Manager):
    def available(self):
        """
        Return only programs that are currently available.
        """
        return self.filter(is_available=True)

    def featured(self):
        """
        Return only available programs that are also marked featured.
        """
        return self.available().filter(is_featured=True)

    def by_region(self, region):
        """
        Return available programs in one region.
        """
        return self.available().filter(region=region)

    def by_category(self, category):
        """
        Return available programs in one category.
        """
        return self.available().filter(category=category)

    def search(self, query):
        """
        Search available programs by:
        - program name
        - organisation name
        - short description
        """
        return self.available().filter(
            Q(name__icontains=query)
            | Q(organisation__name__icontains=query)
            | Q(short_description__icontains=query)
        )

    def for_age(self, age):
        """
        Return available programs suitable for a given age.
        """
        return self.available().filter(age_min__lte=age, age_max__gte=age)



# CRIME DATA MANAGER

# This manager is used by imported crime dataset records.

class CrimeDataManager(models.Manager):
    def by_region(self, region):
        return self.filter(region=region)

    def by_year(self, year):
        return self.filter(year=year)

    def by_offence(self, category):
        return self.filter(offence_category=category)

    def total_by_region(self):
        return (
            self.values("region")
            .annotate(total=Sum("count"))
            .order_by("-total")
        )

    def total_by_year(self):
        return (
            self.values("year")
            .annotate(total=Sum("count"))
            .order_by("year")
        )

    def total_by_category(self):
        return (
            self.values("offence_category")
            .annotate(total=Sum("count"))
            .order_by("-total")
        )


# ENGAGEMENT DATA MANAGER

# Used for imported Closing the Gap / engagement dataset records.

class EngagementDataManager(models.Manager):
    def by_year(self, year):
        return self.filter(year=year)

    def indigenous_only(self):
        return self.filter(
            indigenous_status="Aboriginal and Torres Strait Islander people"
        )

    def non_indigenous_only(self):
        return self.filter(indigenous_status="Non-Indigenous people")

    def by_sex(self, sex):
        return self.filter(sex=sex)

    def nt_trend(self):
        return (
            self.indigenous_only()
            .filter(sex="All people")
            .values("year", "value_nt")
            .order_by("year")
        )