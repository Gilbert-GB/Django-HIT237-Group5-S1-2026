from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .forms import ProgramForm
from .models import Program

from django.http import JsonResponse
from django.db.models import Sum
from youthjustice_app.models import CrimeData
from .models import CrimeData
from django.shortcuts import render
from django.http import JsonResponse
from youthjustice_app.dashboard_service import DashboardService
from django.shortcuts import render, redirect
from .forms import ProgramForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Program

class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    fields = [
        "name",
        "region",
        "category",
        "age_min",
        "age_max",
        "short_description",
        "website",
    ]
    template_name = "youthjustice_app/add_program.html"
    success_url = "/programs/"
    def form_valid(self, form):
        form.instance.organisation = self.request.user.username
        return super().form_valid(form)

def add_program(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)

            # link to logged-in organisation
            if request.user.is_authenticated:
                try:
                    program.owner = request.user.organisation_profile
                except:
                    pass

            program.save()
            return redirect("programs")
    else:
        form = ProgramForm()

    return render(request, "youthjustice_app/add_program.html", {"form": form})

class DashboardView(TemplateView):
    template_name = "youthjustice_app/dashboard.html"

def dashboard_data(request):

    region = request.GET.get("region")
    year = request.GET.get("year")

    data = CrimeData.objects.all()

    # 🎯 FILTERS
    if region:
        data = data.filter(region=region)

    if year:
        data = data.filter(year=year)

    # 📊 Monthly trend
    monthly_trend = list(
        data.values("year", "month")
        .annotate(total_crimes=Sum("count"))
        .order_by("year", "month")
    )

    # 📍 Top regions (bar chart)
    top_regions = list(
        data.values("region")
        .annotate(total=Sum("count"))
        .order_by("-total")[:10]
    )

    # 🥧 Crime categories (pie chart)
    category_breakdown = list(
        data.values("offence_category")
        .annotate(total=Sum("count"))
        .order_by("-total")[:10]
    )

    # 🧠 KPIs
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

def dashboard_page(request):
    return render(request, "dashboard.html")

def home(request):
    # only showing featured programs on home page
    featured_programs = Program.objects.filter(is_featured=True)

    # numbers for the home page cards
    total_programs = Program.objects.count()
    total_featured = Program.objects.filter(is_featured=True).count()
    total_available = Program.objects.filter(is_available=True).count()

    context = {
        "featured_programs": featured_programs,
        "total_programs": total_programs,
        "total_featured": total_featured,
        "total_available": total_available,
    }

    return render(request, "home.html", context)


def programs(request):
    # getting values from the URL
    search_query = request.GET.get("search", "")
    selected_region = request.GET.get("region", "")
    selected_category = request.GET.get("category", "")
    selected_sort = request.GET.get("sort", "")

    programs = Program.objects.all()

    # search by program name
    if search_query:
        programs = programs.filter(name__icontains=search_query)

    # filter by region
    if selected_region:
        programs = programs.filter(region=selected_region)

    # filter by category
    if selected_category:
        programs = programs.filter(category=selected_category)

    # sorting options
    if selected_sort == "name_asc":
        programs = programs.order_by("name")
    elif selected_sort == "name_desc":
        programs = programs.order_by("-name")

    context = {
        "programs": programs,
        "search_query": search_query,
        "selected_region": selected_region,
        "selected_category": selected_category,
        "selected_sort": selected_sort,
        "region_choices": Program.REGION_CHOICES,
        "category_choices": Program.CATEGORY_CHOICES,
    }

    return render(request, "programs.html", context)


def program_detail(request, program_id):
    # showing one program based on id
    program = get_object_or_404(Program, id=program_id)
    return render(request, "program_detail.html", {"program": program})


def about(request):
    return render(request, "about.html")
