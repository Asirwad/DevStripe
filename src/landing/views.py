from django.shortcuts import render

from visits.models import PageVisit
from dashboard.views import dashboard_view

# Create your views here.
def landing_dashboard_page_view(request):
    qs = PageVisit.objects.all()
    if request.user.is_authenticated:
        return dashboard_view(request)
    PageVisit.objects.create(path=request.path)
    return render(request, "landing/main.html", {
        "page_visit_count": qs.count(),
    })