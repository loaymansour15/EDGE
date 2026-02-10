from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from .serializers import *

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from subscriptions.decorators import subscription_required


@api_view(["GET"])
@permission_classes([AllowAny])
def topics_list(request):
    topics = Topic.objects.all().order_by("id")
    data = TopicSerializer(topics, many=True).data
    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def lessons_by_topic(request, topic_id):
    lessons = Lesson.objects.filter(topic_id=topic_id).order_by("id")
    data = LessonSerializer(lessons, many=True).data
    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def quiz_by_lesson(request, lesson_id):
    questions = MCQ.objects.filter(lesson_id=lesson_id).order_by("id")
    data = MCQSerializer(questions, many=True).data
    return Response(data)


@subscription_required
@login_required
def topics_page(request):
    topics = Topic.objects.all().order_by("id")
    return render(request, "topics.html", {"topics": topics})

@subscription_required
@login_required
def lessons_page(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    lessons = Lesson.objects.filter(topic=topic).order_by("id")

    passed_lesson_ids = set(
        LessonProgress.objects.filter(
            user=request.user,
            lesson__in=lessons,
            passed=True
        ).values_list("lesson_id", flat=True)
    )

    return render(request, "lessons.html", {
        "topic": topic,
        "lessons": lessons,
        "passed_lesson_ids": passed_lesson_ids,
    })


@subscription_required
@login_required
def quiz_page(request, lesson_id):
    questions = MCQ.objects.filter(lesson_id=lesson_id)

    if request.method == "POST":
        score = 0
        total = questions.count() 
        print("Total questions:", total)  # Debug print


        wrong_answers = []
        for index, q in enumerate(questions, start=1):
            user_answer = request.POST.get(f"question_{q.id}")

            if user_answer != q.correct_answer:
                wrong_answers.append({
                    "number": index,   # 👈 ده الحل
                    "question": q.question,
                    "user_answer": user_answer,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                })
            else:
                score += 1


        passed = score >= max(1, total * 0.6)

        lesson = questions.first().lesson

        if passed:
            LessonProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={"passed": True}
            )

    
        return render(
            request,
            "quiz_result.html", 
            {
            "score": score,
            "total": total,
            "passed": passed,
            "topic": lesson.topic,
            "topic_id": lesson.topic.id,
            "wrong_answers": wrong_answers
            }
        )



    return render(
        request,
        "quiz.html",
        {
            "questions": questions,
            "lesson_id": lesson_id,
        }
    )
