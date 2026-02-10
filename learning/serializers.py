from rest_framework import serializers
from .models import *


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "is_locked"]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "video_url"]

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ["id", "question", "options"]