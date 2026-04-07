from django.shortcuts import render, get_object_or_404
from .models import Program


def home(request):
    # getting values from the URL (like search text or filters)
    search_query = request.GET.get("search", "")
    selected_region = request.GET.get("region", "")
    selected_category = request.GET.get("category", "")
    selected_sort = request.GET.get("sort", "")

    programs = Program.objects.all()  # start by showing all programs

    # if user types something in search, filter by program name
    if search_query:
        programs = programs.filter(name__icontains=search_query)

    # filter by selected region
    if selected_region:
        programs = programs.filter(region=selected_region)

    # filter by selected category
    if selected_category:
        programs = programs.filter(category=selected_category)

    # sorting based on user choice
    if selected_sort == "name_asc":
        programs = programs.order_by("name")   # A to Z
    elif selected_sort == "name_desc":
        programs = programs.order_by("-name")  # Z to A

    # getting featured programs separately for homepage
    featured_programs = Program.objects.filter(is_featured=True)

    # basic numbers to show on homepage
    total_programs = Program.objects.count()
    total_featured = Program.objects.filter(is_featured=True).count()
    total_available = Program.objects.filter(is_available=True).count()

    context = {
        "programs": programs,
        "featured_programs": featured_programs,
        "search_query": search_query,
        "selected_region": selected_region,
        "selected_category": selected_category,
        "selected_sort": selected_sort,
        "region_choices": Program.REGION_CHOICES,
        "category_choices": Program.CATEGORY_CHOICES,
        "total_programs": total_programs,
        "total_featured": total_featured,
        "total_available": total_available,
    }

    return render(request, "home.html", context)


def program_detail(request, program_id):
    # showing one program based on its id
    program = get_object_or_404(Program, id=program_id)
    return render(request, "program_detail.html", {"program": program})