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
