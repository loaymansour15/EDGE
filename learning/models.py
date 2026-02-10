from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=50)
    is_locked = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=100)
    video_url = models.URLField()

    def __str__(self):
        return self.title


class MCQ(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=20)
    explanation = models.TextField(
        help_text="Explanation shown if the user answers incorrectly"
    )

    def __str__(self):
        return self.question

from django.contrib.auth.models import User

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "lesson")
