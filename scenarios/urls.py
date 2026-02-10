

from django.urls import path
from .views import *

urlpatterns = [
    # FRONTEND
    path("scenarios/<int:topic_id>/", scenarios_page, name="scenarios_page"),
    path("dashboard/", dashboard_page, name="dashboard_page"),

    # API
    path("api/scenarios/<int:topic_id>/", scenarios_by_topic),
    path("api/scenario/submit/", submit_scenario),
    path("api/dashboard/", dashboard),
]




