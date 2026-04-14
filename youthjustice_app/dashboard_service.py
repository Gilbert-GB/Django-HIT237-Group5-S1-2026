from django.db.models import Sum
from youthjustice_app.models import CrimeData

from django.views.generic import TemplateView


class DashboardService:
    """
    Handles all dashboard-related data queries using Django QuerySets.
    Keeps views clean and follows 'less code' philosophy.
    """

    @staticmethod
    def get_monthly_trend():
        return list(
            CrimeData.objects
            .values("year", "month")
            .annotate(total_crimes=Sum("count"))
            .order_by("year", "month")
        )

    @staticmethod
    def get_top_regions(limit=10):
        return list(
            CrimeData.objects
            .values("region")
            .annotate(total=Sum("count"))
            .order_by("-total")[:limit]
        )

    @staticmethod
    def get_category_breakdown():
        return list(
            CrimeData.objects
            .values("offence_category")
            .annotate(total=Sum("count"))
            .order_by("-total")
        )

    @staticmethod
    def get_alcohol_stats():
        return list(
            CrimeData.objects
            .exclude(alcohol_involvement="-")
            .values("alcohol_involvement")
            .annotate(total=Sum("count"))
        )

    @staticmethod
    def get_dv_stats():
        return list(
            CrimeData.objects
            .values("dv_involvement")
            .annotate(total=Sum("count"))
        )

    @staticmethod
    def get_top_offences(limit=10):
        return list(
            CrimeData.objects
            .values("offence_type")
            .annotate(total=Sum("count"))
            .order_by("-total")[:limit]
        )

    @staticmethod
    def get_yearly_trend():
        return list(
            CrimeData.objects
            .values("year")
            .annotate(total=Sum("count"))
            .order_by("year")
        )

    @staticmethod
    def get_kpis():
        total_crimes = CrimeData.objects.aggregate(total=Sum("count"))["total"] or 0

        top_region = (
            CrimeData.objects
            .values("region")
            .annotate(total=Sum("count"))
            .order_by("-total")
            .first()
        )

        top_crime = (
            CrimeData.objects
            .values("offence_type")
            .annotate(total=Sum("count"))
            .order_by("-total")
            .first()
        )

        return {
            "total_crimes": total_crimes,
            "top_region": top_region,
            "top_crime": top_crime,
        }
    @staticmethod
    def get_filtered_by_region(region):
        return list(
            CrimeData.objects
            .filter(region=region)
            .values("year", "month")
            .annotate(total_crimes=Sum("count"))
            .order_by("year", "month")
        )