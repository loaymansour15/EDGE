from django.urls import path
from .views import *

urlpatterns = [

    #path("pricing/", pricing_page, name="pricing"),
    path("pricing/<int:plan_id>/", pricing_page, name="pricing"),

    path("pending/", instapay_pending, name="instapay_pending"),
    path("/subscribe/status/", check_subscription_status, name="check_subscription_status"),
    path("/subscribe/success/", success_page, name="subscription_success"),

    # urls.py
    path("/subscribe/support/", support_page, name="support"),

]
