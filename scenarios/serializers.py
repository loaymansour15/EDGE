from rest_framework import serializers
from .models import Scenario


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = [
            "id",
            "title",
            "market_context",
            "chart_data",
            "difficulty",
        ]


class ScenarioSubmitSerializer(serializers.Serializer):
    scenario_id = serializers.IntegerField()
    choice = serializers.ChoiceField(choices=["SHORT", "LONG", "NO_TRADE"])
