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