from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

@login_required
def profile_list_view(request, *args, **kwargs):
    context = {
        "object_list": User.objects.filter(is_active=True)
    }
    return render(request, "profiles/list.html", context)


@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
    user = request.user

    profile_user_object = get_object_or_404(User, username=username)

    is_me = profile_user_object == user
    context = {
        "object_list": profile_user_object,
        "instance": profile_user_object,
        "owner": is_me,
    }
    return render(request, "profiles/detail.html", context)