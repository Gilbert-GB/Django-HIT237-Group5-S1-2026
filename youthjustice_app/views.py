from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ProgramForm
from .models import Program, CrimeData


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
    Public program list page.
    """

    search_query = request.GET.get("search", "").strip()
    selected_region = request.GET.get("region", "").strip()
    selected_category = request.GET.get("category", "").strip()
    selected_sort = request.GET.get("sort", "").strip()

    program_list = Program.objects.available().select_related("organisation")

    if search_query:
        program_list = Program.objects.search(search_query).select_related("organisation")

    if selected_region:
        program_list = program_list.filter(region=selected_region)

    if selected_category:
        program_list = program_list.filter(category=selected_category)

    # Sorting
    if selected_sort == "name_asc":
        program_list = program_list.order_by("name")
    elif selected_sort == "name_desc":
        program_list = program_list.order_by("-name")

    context = {
        "programs": program_list,
        "search_query": search_query,
        "selected_region": selected_region,
        "selected_category": selected_category,
        "selected_sort": selected_sort,
        "region_choices": Program.REGION_CHOICES,
        "category_choices": Program.CATEGORY_CHOICES,
    }
    return render(request, "youthjustice_app/programs.html", context)


def program_detail(request, pk):
    program = get_object_or_404(
        Program.objects.select_related("organisation"),
        pk=pk
    )
    return render(
        request,
        "youthjustice_app/program_detail.html",
        {"program": program},
    )


def about(request):
    return render(request, "youthjustice_app/about.html")


# DASHBOARD

def dashboard_page(request):
    return render(request, "youthjustice_app/dashboard.html")


def dashboard_data(request):
    """
    Filters:
    - region
    - year
    """

    region = request.GET.get("region")
    year = request.GET.get("year")

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
    
# MANAGEMENT / CRUD Section

# Class-based views for managing programs (CRUD)
# Uses reverse_lazy to redirect back to manage_programs after successful creation, update, or deletion

class ProgramManageListView(ListView):
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


class ProgramCreateView(CreateView):
    """
    Create a new program.
    Uses ProgramForm automatically
    """
    model = Program
    form_class = ProgramForm
    template_name = "youthjustice_app/add_program.html"
    success_url = reverse_lazy("manage_programs")


class ProgramUpdateView(UpdateView):
    """
    Editing an existing program.
    Reuses the same form as the create view.
    """
    model = Program
    form_class = ProgramForm
    template_name = "youthjustice_app/edit_program.html"
    success_url = reverse_lazy("manage_programs")


class ProgramDeleteView(DeleteView):
    """
    Delete an existing program
    """
    model = Program
    template_name = "youthjustice_app/delete_program.html"
    success_url = reverse_lazy("manage_programs")