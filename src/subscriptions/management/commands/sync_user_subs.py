from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.models import UserSubscription
from customers.models import Customer
import helpers.billing

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
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