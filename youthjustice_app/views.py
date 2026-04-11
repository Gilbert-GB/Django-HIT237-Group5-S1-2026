from django.shortcuts import render, get_object_or_404

from .forms import OrganisationRegisterForm, ProgramForm
from .models import Program

from django.http import JsonResponse
from django.db.models import Sum
from youthjustice_app.models import CrimeData
from .models import CrimeData
from django.shortcuts import render

def dashboard_page(request):
    return render(request, "dashboard.html")

def dashboard_data(request):
    from django.db.models import Sum
    from django.http import JsonResponse
    from .models import CrimeData

    # 📊 Monthly Crime Trend
    monthly_trend = list(
        CrimeData.objects
        .values("year", "month")
        .annotate(total_crimes=Sum("count"))
        .order_by("year", "month")
    )

    # 📍 Top Regions
    top_regions = list(
        CrimeData.objects
        .values("region")
        .annotate(total=Sum("count"))
        .order_by("-total")[:10]
    )

    # 🚨 Category Breakdown
    category_breakdown = list(
        CrimeData.objects
        .values("offence_category")
        .annotate(total=Sum("count"))
        .order_by("-total")
    )

    # 🍺 Alcohol Stats
    alcohol_stats = list(
        CrimeData.objects
        .exclude(alcohol_involvement="-")
        .values("alcohol_involvement")
        .annotate(total=Sum("count"))
    )

    # ⚠️ DV Stats
    dv_stats = list(
        CrimeData.objects
        .values("dv_involvement")
        .annotate(total=Sum("count"))
    )

    # 🔝 Top Offences
    top_offences = list(
        CrimeData.objects
        .values("offence_type")
        .annotate(total=Sum("count"))
        .order_by("-total")[:10]
    )

    # 📈 Yearly Trend
    yearly_trend = list(
        CrimeData.objects
        .values("year")
        .annotate(total=Sum("count"))
        .order_by("year")
    )

    # 🧠 KPIs
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

    data = {
        "kpis": {
            "total_crimes": total_crimes,
            "top_region": top_region,
            "top_crime": top_crime,
        },
        "charts": {
            "monthly_trend": monthly_trend,
            "top_regions": top_regions,
            "category_breakdown": category_breakdown,
            "alcohol_stats": alcohol_stats,
            "dv_stats": dv_stats,
            "top_offences": top_offences,
            "yearly_trend": yearly_trend,
        }
    }

    return JsonResponse(data)

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