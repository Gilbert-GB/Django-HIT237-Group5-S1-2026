from django.shortcuts import render
from .models import Program


def home(request):
    search_query = request.GET.get("search", "")

    if search_query:
        programs = Program.objects.filter(name__icontains=search_query)
    else:
        programs = Program.objects.all()

    featured_programs = Program.objects.filter(is_featured=True)

    context = {
        "programs": programs,
        "featured_programs": featured_programs,
        "search_query": search_query,
    }

    return render(request, "home.html", context) 