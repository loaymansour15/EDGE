from django.conf import settings
from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")

    is_active = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return (
            self.is_active
            and self.expires_at is not None
            and self.expires_at > timezone.now()
        )

    def __str__(self):
        status = "Active" if self.is_valid() else "Inactive"
        return f"{self.user} - {status}"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()  # بالجنيه
    paymob_order_id = models.CharField(max_length=100, blank=True, null=True)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} EGP"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price_egp = models.IntegerField()
    duration_days = models.IntegerField()  # مدة الاشتراك بالأيام
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price_egp} EGP"


class ManualPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    reference_code = models.CharField(max_length=50, unique=True)
    proof = models.ImageField(upload_to="payments/")
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
