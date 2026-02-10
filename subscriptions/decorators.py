from django.shortcuts import redirect
from django.urls import reverse
from .models import Subscription


def subscription_required(view_func):
    def _wrapped(request, *args, **kwargs):
        sub = Subscription.objects.filter(user=request.user).first()
        if not sub or not sub.is_valid():
            return redirect(reverse("pricing", kwargs={"plan_id": 1}))  # Redirect to pricing page with a default plan
        return view_func(request, *args, **kwargs)
    return _wrapped
