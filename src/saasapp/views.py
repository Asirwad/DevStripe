from django.http import HttpResponse
import pathlib
from django.shortcuts import render

from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

def home_page_view(request, *args, **kwargs):
    queryset = PageVisit.objects.all()
    page_queryset = PageVisit.objects.filter(path=request.path)
    my_name = "Asirwad Sali"
    my_context = {
        "my_name": my_name,
        "page_visit_count": page_queryset.count(),
        "total_visit_count": queryset.count(),
        "percent": (page_queryset.count()*100) / queryset.count(),
    }
    path = request.path
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)