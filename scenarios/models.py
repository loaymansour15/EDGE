from django.db import models
from django.contrib.auth.models import User
from learning.models import Topic


class Scenario(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="scenarios")
    title = models.CharField(max_length=100)

    order = models.PositiveIntegerField(default=1)  # 👈 جديد

    decision_index = models.PositiveIntegerField(default=0)


    market_context = models.TextField()
    chart_data = models.JSONField()
    correct_choice = models.CharField(max_length=20)

    difficulty = models.CharField(
        max_length=20,
        choices=[("easy","Easy"),("medium","Medium"),("hard","Hard")],
        default="easy"
    )

    class Meta:
        ordering = ["order"]  # 👈 ترتيب تلقائي

    def __str__(self):
        return f"{self.order} - {self.title}"


class ScenarioResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    user_choice = models.CharField(max_length=20)
    score = models.IntegerField()

    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title}"
