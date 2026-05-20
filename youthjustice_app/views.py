from django.db.models import Sum
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
from django.http import HttpResponse

from .forms import ProgramForm
from .models import Program, CrimeData, EngagementData, Organisation


# PUBLIC PAGES

def home(request):
    """
    Home page:
    """

    featured_programs = (
        Program.objects.featured()
        .select_related("organisation")
    )

    total_programs = Program.objects.count()
    total_featured = Program.objects.featured().count()
    total_available = Program.objects.available().count()

    context = {
        "featured_programs": featured_programs,
        "total_programs": total_programs,
        "total_featured": total_featured,
        "total_available": total_available,
    }
    return render(request, "youthjustice_app/home.html", context)


def programs(request):
    """
    Public program list page with search, filter, sort, and pagination.
    """

    search_query = request.GET.get("search", "").strip()
    selected_region = request.GET.get("region", "").strip()
    selected_category = request.GET.get("category", "").strip()
    selected_sort = request.GET.get("sort", "").strip()
    selected_age = request.GET.get("age", "").strip()

    program_list = Program.objects.available().select_related("organisation")

    if search_query:
        program_list = Program.objects.search(search_query).select_related("organisation")

    if selected_region:
        program_list = program_list.filter(region=selected_region)

    if selected_category:
        program_list = program_list.filter(category=selected_category)
    # Filter by age — show programs that accept this age
    if selected_age:
        try:
            age_value = int(selected_age)
            program_list = program_list.filter(age_min__lte=age_value, age_max__gte=age_value)
        except ValueError:
            pass

    # Sorting
    if selected_sort == "name_asc":
        program_list = program_list.order_by("name")
    elif selected_sort == "name_desc":
        program_list = program_list.order_by("-name")

    # Pagination — 9 programs per page (3x3 grid)
    paginator = Paginator(program_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "programs": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "selected_region": selected_region,
        "selected_category": selected_category,
        "selected_sort": selected_sort,
        "selected_age": selected_age,
        "region_choices": Program.REGION_CHOICES,
        "category_choices": Program.CATEGORY_CHOICES,
    }
    return render(request, "youthjustice_app/programs.html", context)


def program_detail(request, pk):
    """
    Shows one program with related programs from same region and category.
    """
    program = get_object_or_404(
        Program.objects.select_related("organisation"),
        pk=pk
    )

    # Programs in the same region (excluding current one)
    same_region = (
        Program.objects.available()
        .filter(region=program.region)
        .exclude(pk=program.pk)
        .select_related("organisation")
        [:4]
    )

    # Programs in the same category (excluding current + already shown in region)
    shown_ids = [p.pk for p in same_region]
    shown_ids.append(program.pk)

    same_category = (
        Program.objects.available()
        .filter(category=program.category)
        .exclude(pk__in=shown_ids)
        .select_related("organisation")
        [:4]
    )

    context = {
        "program": program,
        "same_region": same_region,
        "same_category": same_category,
    }
    return render(request, "youthjustice_app/program_detail.html", context)


def about(request):
    return render(request, "youthjustice_app/about.html")

def organisation_list(request):
    """
    Lists all organisations with their program count.
    """
    from django.db.models import Count

    selected_type = request.GET.get("type", "").strip()

    organisations = Organisation.objects.annotate(
        program_count=Count("programs")
    ).order_by("name")

    if selected_type:
        organisations = organisations.filter(organisation_type=selected_type)

    context = {
        "organisations": organisations,
        "selected_type": selected_type,
        "type_choices": Organisation.ORG_TYPE_CHOICES,
    }
    return render(request, "youthjustice_app/organisations.html", context)


def organisation_detail(request, pk):
    """
    Shows one organisation and all its programs.
    """
    organisation = get_object_or_404(Organisation, pk=pk)

    org_programs = organisation.programs.filter(is_available=True).order_by("name")

    context = {
        "organisation": organisation,
        "programs": org_programs,
        "total_programs": organisation.programs.count(),
        "available_programs": org_programs.count(),
    }
    return render(request, "youthjustice_app/organisation_detail.html", context)


# DASHBOARD

def dashboard_page(request):
    return render(request, "youthjustice_app/dashboard.html")


def dashboard_data(request):
    """
    JSON API endpoint for crime dashboard.
    Uses DashboardService for clean separation of query logic.
    """
    from .dashboard_service import DashboardService

    region = request.GET.get("region")
    year = request.GET.get("year")

    # If filters are active, use filtered queries
    if region or year:
        data = CrimeData.objects.all()

        if region:
            data = data.filter(region=region)
        if year:
            data = data.filter(year=year)

        monthly_trend = list(
            data.values("year", "month")
            .annotate(total_crimes=Sum("count"))
            .order_by("year", "month")
        )

        top_regions = list(
            data.values("region")
            .annotate(total=Sum("count"))
            .order_by("-total")[:10]
        )

        category_breakdown = list(
            data.values("offence_category")
            .annotate(total=Sum("count"))
            .order_by("-total")[:10]
        )

        total_crimes = data.aggregate(total=Sum("count"))["total"] or 0

        top_region = (
            data.values("region")
            .annotate(total=Sum("count"))
            .order_by("-total")
            .first()
        )

        top_crime = (
            data.values("offence_type")
            .annotate(total=Sum("count"))
            .order_by("-total")
            .first()
        )

        return JsonResponse({
            "kpis": {
                "total_crimes": total_crimes,
                "top_region": top_region,
                "top_crime": top_crime,
            },
            "charts": {
                "monthly_trend": monthly_trend,
                "top_regions": top_regions,
                "category_breakdown": category_breakdown,
            }
        })

    # No filters — use DashboardService (clean, reusable)
    kpis = DashboardService.get_kpis()

    return JsonResponse({
        "kpis": kpis,
        "charts": {
            "monthly_trend": DashboardService.get_monthly_trend(),
            "top_regions": DashboardService.get_top_regions(),
            "category_breakdown": DashboardService.get_category_breakdown(),
        },
        "extra": {
            "yearly_trend": DashboardService.get_yearly_trend(),
            "alcohol_stats": DashboardService.get_alcohol_stats(),
            "dv_stats": DashboardService.get_dv_stats(),
            "top_offences": DashboardService.get_top_offences(),
        }
    })


def engagement_data(request):
    """
    JSON API endpoint for engagement dashboard.
    Returns Closing the Gap data filtered by year, sex, indigenous status.
    """

    selected_year = request.GET.get("year")
    selected_sex = request.GET.get("sex")
    selected_status = request.GET.get("status")

    data = EngagementData.objects.all()

    if selected_year:
        data = data.filter(year=int(selected_year))

    if selected_sex:
        data = data.filter(sex=selected_sex)

    if selected_status == "indigenous":
        data = EngagementData.objects.indigenous_only()
        if selected_year:
            data = data.filter(year=int(selected_year))
        if selected_sex:
            data = data.filter(sex=selected_sex)
    elif selected_status == "non_indigenous":
        data = EngagementData.objects.non_indigenous_only()
        if selected_year:
            data = data.filter(year=int(selected_year))
        if selected_sex:
            data = data.filter(sex=selected_sex)

    # NT trend over years (for line chart)
    nt_trend = list(
        data.values("year")
        .annotate(avg_nt=models.Avg("value_nt"), avg_national=models.Avg("value_national"))
        .order_by("year")
    )

    # Breakdown by sex (for bar chart)
    by_sex = list(
        data.exclude(sex="All people")
        .values("sex")
        .annotate(avg_nt=models.Avg("value_nt"), avg_national=models.Avg("value_national"))
    )

    # Breakdown by indigenous status (for comparison chart)
    by_status = list(
        data.values("indigenous_status")
        .annotate(avg_nt=models.Avg("value_nt"), avg_national=models.Avg("value_national"))
    )

    # Available years for filter dropdown
    available_years = sorted(
        data.values_list("year", flat=True).distinct()
    )

    # KPIs
    latest_year = data.order_by("-year").values_list("year", flat=True).first()
    latest_data = data.filter(year=latest_year) if latest_year else data.none()

    indigenous_nt = latest_data.filter(
        indigenous_status="Aboriginal and Torres Strait Islander people",
        sex="All people"
    ).values_list("value_nt", flat=True).first()

    non_indigenous_nt = latest_data.filter(
        indigenous_status="Non-Indigenous people",
        sex="All people"
    ).values_list("value_nt", flat=True).first()

    gap_value = None
    if indigenous_nt is not None and non_indigenous_nt is not None:
        gap_value = round(indigenous_nt - non_indigenous_nt, 1)

    return JsonResponse({
        "kpis": {
            "latest_year": latest_year,
            "indigenous_nt": indigenous_nt,
            "non_indigenous_nt": non_indigenous_nt,
            "gap": gap_value,
        },
        "charts": {
            "nt_trend": nt_trend,
            "by_sex": by_sex,
            "by_status": by_status,
        },
        "available_years": available_years,
    })

def export_programs_csv(request):
    """
    Exports filtered programs as a downloadable CSV file.
    Uses the same filters as the programs page.
    """

    search_query = request.GET.get("search", "").strip()
    selected_region = request.GET.get("region", "").strip()
    selected_category = request.GET.get("category", "").strip()
    selected_age = request.GET.get("age", "").strip()

    program_list = Program.objects.available().select_related("organisation")

    if search_query:
        program_list = Program.objects.search(search_query).select_related("organisation")

    if selected_region:
        program_list = program_list.filter(region=selected_region)

    if selected_category:
        program_list = program_list.filter(category=selected_category)

    if selected_age:
        try:
            age_value = int(selected_age)
            program_list = program_list.filter(age_min__lte=age_value, age_max__gte=age_value)
        except ValueError:
            pass

    # Build CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="youth_justice_programs.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Program Name",
        "Organisation",
        "Region",
        "Category",
        "Age Min",
        "Age Max",
        "Available",
        "Description",
        "Website",
    ])

    for program in program_list:
        writer.writerow([
            program.name,
            program.organisation.name,
            program.get_region_display(),
            program.get_category_display(),
            program.age_min,
            program.age_max,
            "Yes" if program.is_available else "No",
            program.short_description,
            program.website or "",
        ])

    return response


def export_crime_csv(request):
    """
    Exports filtered crime data as a downloadable CSV file.
    Uses the same filters as the dashboard.
    """

    region = request.GET.get("region", "").strip()
    year = request.GET.get("year", "").strip()
    category = request.GET.get("category", "").strip()

    data = CrimeData.objects.all()

    if region:
        data = data.filter(region=region)

    if year:
        data = data.filter(year=int(year))

    if category:
        data = data.filter(offence_category=category)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="nt_crime_data.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Year",
        "Month",
        "Month Name",
        "Region",
        "Offence Category",
        "Offence Type",
        "Alcohol Involvement",
        "DV Involvement",
        "Count",
    ])

    for record in data:
        writer.writerow([
            record.year,
            record.month,
            record.month_name,
            record.region,
            record.offence_category_short,
            record.offence_type,
            record.alcohol_involvement,
            record.dv_involvement,
            record.count,
        ])

    return response


def export_engagement_csv(request):
    """
    Exports filtered engagement data as a downloadable CSV file.
    """

    selected_year = request.GET.get("year", "").strip()
    selected_sex = request.GET.get("sex", "").strip()
    selected_status = request.GET.get("status", "").strip()

    data = EngagementData.objects.all()

    if selected_year:
        data = data.filter(year=int(selected_year))

    if selected_sex:
        data = data.filter(sex=selected_sex)

    if selected_status == "indigenous":
        data = data.filter(indigenous_status="Aboriginal and Torres Strait Islander people")
    elif selected_status == "non_indigenous":
        data = data.filter(indigenous_status="Non-Indigenous people")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="closing_the_gap_engagement.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Year",
        "Sex",
        "Indigenous Status",
        "Measure",
        "NT Value (%)",
        "National Value (%)",
        "Gap (%)",
    ])

    for record in data:
        writer.writerow([
            record.year,
            record.sex,
            record.indigenous_status,
            record.measure,
            record.nt_display,
            record.national_display,
            record.gap_display,
        ])

    return response
def engagement_page(request):
    return render(request, "youthjustice_app/engagement.html")
# MANAGEMENT / CRUD Section

# Class-based views for managing programs (CRUD)
# Uses reverse_lazy to redirect back to manage_programs after successful creation, update, or deletion

class ProgramManageListView(LoginRequiredMixin, ListView):
    """
    Shows all programs in one place for easy management and appealing UI
    """
    model = Program
    template_name = "youthjustice_app/manage_programs.html"
    context_object_name = "programs"
    ordering = ["name"]

    def get_queryset(self):
        """
        select_related('organisation')
        """
        return Program.objects.select_related("organisation").all().order_by("name")


class ProgramCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new program.
    Uses ProgramForm automatically
    """
    model = Program
    form_class = ProgramForm
    template_name = "youthjustice_app/add_program.html"
    success_url = reverse_lazy("manage_programs")


class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    """
    Editing an existing program.
    Reuses the same form as the create view.
    """
    model = Program
    form_class = ProgramForm
    template_name = "youthjustice_app/edit_program.html"
    success_url = reverse_lazy("manage_programs")


class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an existing program
    """
    model = Program
    template_name = "youthjustice_app/delete_program.html"
    success_url = reverse_lazy("manage_programs")
