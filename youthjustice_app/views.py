from django.shortcuts import render, get_object_or_404
from .models import Program


def home(request):
    search_query = request.GET.get("search", "")
    selected_region = request.GET.get("region", "")
    selected_category = request.GET.get("category", "")

    programs = Program.objects.all()

    if search_query:
        programs = programs.filter(name__icontains=search_query)

    if selected_region:
        programs = programs.filter(region=selected_region)

    if selected_category:
        programs = programs.filter(category=selected_category)

    featured_programs = Program.objects.filter(is_featured=True)

    total_programs = Program.objects.count()
    total_featured = Program.objects.filter(is_featured=True).count()
    total_available = Program.objects.filter(is_available=True).count()

    context = {
        "programs": programs,
        "featured_programs": featured_programs,
        "search_query": search_query,
        "selected_region": selected_region,
        "selected_category": selected_category,
        "region_choices": Program.REGION_CHOICES,
        "category_choices": Program.CATEGORY_CHOICES,
        "total_programs": total_programs,
        "total_featured": total_featured,
        "total_available": total_available,
    }

    return render(request, "home.html", context)


def program_detail(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    return render(request, "program_detail.html", {"program": program})