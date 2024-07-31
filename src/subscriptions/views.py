from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from subscriptions.models import SubscriptionPrice, UserSubscription
import helpers.billing
from subscriptions import utils as sub_utils

# Create your views here.
@login_required
def user_subscription_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    # sub_data = user_sub_obj.searilize()
    if request.method == "POST":
        finished = sub_utils.refresh_users_subscription(user_ids=[request.user.id])
        if finished: 
            messages.success(request, "Your plan details has been updated!")
        else:
            messages.error(request, "Your plan details has not been updated!")
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, 
                  "subscriptions/user_subscription_detail_view.html",
                  {
                    "subscription": user_sub_obj
                  }
                )

@login_required
def user_subscription_cancel_view(request):
    user_subscription_object, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == "POST":
        if user_subscription_object.stripe_id and user_subscription_object.is_active_status:
            sub_data = helpers.billing.cancel_subscription(
                user_subscription_object.stripe_id, 
                reason="User wanted to end", 
                feedback="other",
                cancel_at_period_end=True,
                raw=False)
            for k, v in sub_data.items():
                setattr(user_subscription_object, k, v)
            user_subscription_object.save()
            messages.success(request, "Subscription Cancelled!")
        return redirect(user_subscription_object.get_absolute_url())
    return render(request, 
                  "subscriptions/user_subscription_cancel_view.html",
                  {
                    "subscription": user_subscription_object
                  }
                )



def subscription_price_view(request,interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoices.YEARLY

    if interval == inv_yr:
        object_list = qs.filter(interval=inv_yr)
        active = inv_yr
    else:
        object_list = qs.filter(interval=inv_mo)
        active = inv_mo

    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name, kwargs={"interval": inv_mo})
    yr_url = reverse(url_path_name, kwargs={"interval": inv_yr})

    return render(request, "subscriptions/pricing.html", {
        "object_list": object_list,
        "mo_url": mo_url,
        "yr_url": yr_url,
        "active": active,
    })