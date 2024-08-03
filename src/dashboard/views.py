from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from subscriptions.models import UserSubscription

# Create your views here.
@login_required
def dashboard_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    return render(request, "dashboard/main.html", {
        "subscription": user_sub_obj
    })