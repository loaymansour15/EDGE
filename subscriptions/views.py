from datetime import timedelta
from time import timezone
from django.conf import settings
from django.shortcuts import redirect, render
from subscriptions.models import *
from django.contrib.auth.decorators import login_required
from .utils import generate_reference
from django.utils import timezone

from django.http import JsonResponse
from .models import SubscriptionPlan

from django.contrib import messages


"""
@login_required
def pricing_page(request):
    sub = Subscription.objects.filter(user=request.user).first()
    is_valid = sub.is_valid() if sub else False

    plans = SubscriptionPlan.objects.filter(is_active=True).order_by("price_egp")

    return render(request, "pricing.html", {
        "sub": sub,
        "is_valid": is_valid,
        "plans": plans,
    })
"""

@login_required
def pricing_page(request, plan_id):

    get_sub = Subscription.objects.filter(user=request.user).first()
    get_last_payment = ManualPayment.objects.filter(is_confirmed=False, user=request.user).first()
    if get_last_payment:
        return redirect("instapay_pending")
    elif get_sub and get_sub.is_active():
        return redirect("dashboard")

    

    plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
    reference = generate_reference(request.user.id)

    if request.method == "POST":
        proof = request.FILES.get("proof")
        reference = request.POST.get("reference")

        ManualPayment.objects.create(
            user=request.user,
            plan=plan,
            reference_code=reference,
            proof=proof,
        )

        return redirect("instapay_pending")

    return render(request, "pricing.html", {
        "plan": plan,
        "reference": reference,
        "receiver": settings.INSTAPAY_RECEIVER,
    })


""""
@login_required
def pricing_page(request):
    amount = settings.MONTHLY_PRICE_EGP
    receiver = settings.INSTAPAY_RECEIVER
    reference = generate_reference(request.user.id)

    if request.method == "POST":
        proof = request.FILES.get("proof")
        reference = request.POST.get("reference")

        if not proof:
            return render(request, "pricing.html", {
                "error": "لازم ترفع صورة التحويل",
                "amount": amount,
                "receiver": receiver,
                "reference": reference,
                "monthly_price_egp": amount,
            })

        ManualPayment.objects.create(
            user=request.user,
            amount_egp=amount,
            reference_code=reference,
            proof=proof,
        )

        return redirect("instapay_pending")

    return render(request, "pricing.html", {
        "amount": amount,
        "receiver": receiver,
        "reference": reference,
        "monthly_price_egp": amount,
    })

"""


@login_required
def instapay_pending(request):
    return render(request, "instapay_pending.html")




@login_required
def check_subscription_status(request):
    sub = Subscription.objects.filter(user=request.user).first()
    is_active = sub.is_active if sub else False
    return JsonResponse({
        "active": is_active
    })

@login_required
def success_page(request):
    return render(request, "subscription_success.html")


@login_required
def support_page(request):
    return render(request, "support.html")







