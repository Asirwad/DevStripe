from django.shortcuts import render

from visits.models import PageVisit

# Create your views here.
def landing_page_view(request):
    qs = PageVisit.objects.all()
    PageVisit.objects.create(path=request.path)
    return render(request, "landing/main.html", {
        "page_visit_count": qs.count(),
    })