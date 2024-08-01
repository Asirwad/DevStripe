from subscriptions.models import UserSubscription, Subscription, SubscriptionStatus
from customers.models import Customer
import helpers.billing

from django.db.models import Q

def refresh_users_subscription(
        user_ids=None, 
        active_only=True, 
        days_ago=0, 
        days_left=0,
        day_start=0,
        day_end=0,
        verbose=False
        ):
    qs = UserSubscription.objects.all()
    if active_only:
        qs = qs.by_active_trailing()
    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    if days_ago>0:
        qs = qs.by_days_ago(days_ago=days_ago)
    if days_left > 0:
        qs = qs.by_days_left(days_left=days_left)
    if day_start > 0 and day_end > 0:
        qs = qs.by_days_range(days_start=day_start, days_end=day_end)
    
    complete_count, qs_count = 0, qs.count()
    for obj in qs:
        if verbose:
            print("Updating user ", obj.user, " ", obj.subscription, " ", obj.current_period_end)
        if obj.stripe_id:
            sub_data = helpers.billing.get_subscription(obj.stripe_id, raw=False)
            for k, v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count+=1
    return complete_count==qs_count

def clear_dangling_subs():
    customers = Customer.objects.filter(stripe_id__isnull=False)
    for customer in customers:
        user = customer.user
        customer_stripe_id = customer.stripe_id
        print(f"Sync {user}-{customer_stripe_id} subs and remove old ones")
        subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs = UserSubscription.objects.filter(stripe_id__iexact=f"{sub.id}".strip())
            if existing_user_subs_qs.exists():
                continue
            helpers.billing.cancel_subscription(
                stripe_id=sub.id, 
                reason="Dangling active subscription",
                cancel_at_period_end=False)
            print(sub.id, existing_user_subs_qs.exists())


def sync_subs_group_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perms)