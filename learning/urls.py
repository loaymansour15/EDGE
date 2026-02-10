from django.urls import path
from .views import *

urlpatterns = [
    #path("topics/", topics_list, name="topics_list"),

    #path("lessons/<int:topic_id>/", lessons_by_topic, name="lessons_by_topic"),

    #path("quiz/<int:lesson_id>/", quiz_by_lesson, name="quiz_by_lesson"),

    # ========= API =========
    path("api/topics/", topics_list),
    path("api/lessons/<int:topic_id>/", lessons_by_topic),
    path("api/quiz/<int:lesson_id>/", quiz_by_lesson),

    path("topics-page/", topics_page, name="topics_page"),
    path("lessons/<int:topic_id>/", lessons_page, name="lessons_page"),
    path("quiz/<int:lesson_id>/", quiz_page),

]
