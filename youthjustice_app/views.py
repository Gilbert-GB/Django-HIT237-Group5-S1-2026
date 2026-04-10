from django.shortcuts import render, get_object_or_404

from .forms import OrganisationRegisterForm, ProgramForm
from .models import Program


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