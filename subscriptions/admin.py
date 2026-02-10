from django.contrib import admin

# Register your models here.
from django.utils import timezone
from datetime import timedelta
from .models import *

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "started_at", "expires_at", "created_at")
    list_filter = ("is_active", "started_at", "expires_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("user", "is_active", "started_at", "expires_at")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

@admin.register(ManualPayment)
class ManualPaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "is_confirmed", "created_at")
    actions = ["confirm_payments"]

    def confirm_payments(self, request, queryset):
        for payment in queryset.filter(is_confirmed=False):
            payment.is_confirmed = True
            payment.save()

            sub, _ = Subscription.objects.get_or_create(user=payment.user)
            sub.is_active = True
            sub.started_at = timezone.now()
            sub.expires_at = timezone.now() + timedelta(days=payment.plan.duration_days)
            sub.save()

        self.message_user(request, "تم تفعيل الاشتراكات بنجاح")


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price_egp", "duration_days", "is_active")
    list_editable = ("price_egp", "duration_days", "is_active")
