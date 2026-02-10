from django.contrib import admin
from .models import *

admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(MCQ)
admin.site.register(LessonProgress)
