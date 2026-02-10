from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.db.models import Avg, Count

from subscriptions.models import SubscriptionPlan

from .models import Scenario, ScenarioResult
from .serializers import ScenarioSerializer, ScenarioSubmitSerializer

from learning.models import LessonProgress

from subscriptions.decorators import subscription_required

# ======================================================
# ======================= API ==========================
# ======================================================

@api_view(["GET"])
@permission_classes([AllowAny])
def scenarios_by_topic(request, topic_id):
    scenarios = Scenario.objects.filter(topic_id=topic_id).order_by("order")
    data = ScenarioSerializer(scenarios, many=True).data
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_scenario(request):
    serializer = ScenarioSubmitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    scenario_id = serializer.validated_data["scenario_id"]
    choice = serializer.validated_data["choice"]

    scenario = get_object_or_404(Scenario, id=scenario_id)

    # ===== Decision Evaluation =====
    if choice == scenario.correct_choice:
        score = 100
        explanation = "Decision aligned with the market context and trend."
        correct = True
    elif choice == "NO_TRADE":
        score = 60
        explanation = "Safe decision, but you missed a valid opportunity."
        correct = False
    else:
        score = 20
        explanation = "Decision was against the market direction."
        correct = False

    # ===== First Attempt Only =====
    existing_result = ScenarioResult.objects.filter(
        user=request.user,
        scenario=scenario
    ).first()

    if not existing_result:
        ScenarioResult.objects.create(
            user=request.user,
            scenario=scenario,
            user_choice=choice,
            score=score,
            explanation=explanation
        )
        counted = True
    else:
        counted = False  # Practice mode

    return Response({
        "correct": correct,
        "score": score,
        "explanation": explanation,
        "counted": counted
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    results = ScenarioResult.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total = results.count()
    avg_score = results.aggregate(avg=Avg("score"))["avg"] or 0

    last_results = [
        {
            "scenario": r.scenario.title,
            "choice": r.user_choice,
            "score": r.score,
            "date": r.created_at,
        }
        for r in results[:10]
    ]

    return Response({
        "total_scenarios": total,
        "average_score": round(avg_score, 2),
        "last_results": last_results
    })


# ======================================================
# ===================== HTML ===========================
# ======================================================


@subscription_required
@login_required
def scenarios_page(request, topic_id):

    # ===============================
    # 1️⃣ منع الدخول لو المستخدم معدّاش الكويز
    # ===============================
    passed_quiz = LessonProgress.objects.filter(
        user=request.user,
        lesson__topic_id=topic_id,
        passed=True
    ).exists()

    if not passed_quiz:
        return render(request, "blocked.html")

    # ===============================
    # 2️⃣ جلب السيناريوهات مرتبة
    # ===============================
    scenarios = Scenario.objects.filter(
        topic_id=topic_id
    ).order_by("order")

    if not scenarios.exists():
        return render(request, "blocked.html")

    # ===============================
    # 3️⃣ تحديد السيناريو الحالي
    # ===============================
    requested_scenario_id = request.GET.get("scenario")

    if requested_scenario_id:
        scenario = get_object_or_404(
            Scenario,
            id=requested_scenario_id,
            topic_id=topic_id
        )

        # السيناريو السابق
        previous_scenario = scenarios.filter(
            order__lt=scenario.order
        ).last()

        # لو السيناريو السابق لم يُحل → اقفل
        if previous_scenario:
            solved = ScenarioResult.objects.filter(
                user=request.user,
                scenario=previous_scenario
            ).exists()

            if not solved:
                return render(request, "blocked.html")

    else:
        scenario = scenarios.first()

    # ===============================
    # 4️⃣ معالجة الإجابة (First Attempt Only)
    # ===============================
    result = None

    if request.method == "POST":
        choice = request.POST.get("choice")

        if choice == scenario.correct_choice:
            score = 100
            explanation = "قرار يتماشى مع سياق السوق واتجاهاته."
            correct = True
        elif choice == "NO_TRADE":
            score = 60
            explanation = "قرار آمن، لكنك فاتت فرصة صحيحة."
            correct = False
        else:
            score = 20
            explanation = "قرار خاطئ وتعارض مع اتجاه السوق."
            correct = False

        existing_result = ScenarioResult.objects.filter(
            user=request.user,
            scenario=scenario
        ).first()

        if not existing_result:
            ScenarioResult.objects.create(
                user=request.user,
                scenario=scenario,
                user_choice=choice,
                score=score,
                explanation=explanation
            )
            counted = True
        else:
            counted = False

        result = {
            "correct": correct,
            "score": score,
            "explanation": explanation,
            "choice": choice,
            "counted": counted
        }

    # ===============================
    # 5️⃣ السيناريو التالي
    # ===============================
    prev_scenario = Scenario.objects.filter(
    topic=scenario.topic,
    order__lt=scenario.order
    ).order_by("-order").first()

    next_scenario = Scenario.objects.filter(
        topic=scenario.topic,
        order__gt=scenario.order
    ).order_by("order").first()


    answered = ScenarioResult.objects.filter(
        user=request.user,
        scenario=scenario
    ).exists()

    # ===============================
    # 6️⃣ Progress
    # ===============================
    total_scenarios = scenarios.count()

    completed_scenarios = ScenarioResult.objects.filter(
        user=request.user,
        scenario__topic_id=topic_id
    ).values("scenario").distinct().count()

    progress_percent = 0
    if total_scenarios > 0:
        progress_percent = int(
            (completed_scenarios / total_scenarios) * 100
        )

    # ===============================
    # 7️⃣ Render
    # ===============================
    return render(
        request,
        "scenario.html",
        {
            "scenario": scenario,
            "result": result,
            "prev_scenario": prev_scenario,
            "next_scenario": next_scenario,
            "answered": answered,
            "total_scenarios": total_scenarios,
            "completed_scenarios": completed_scenarios,
            "progress_percent": progress_percent,
        }
    )


@login_required
def dashboard_page(request):
    user = request.user

    results = ScenarioResult.objects.filter(
        user=user
    ).order_by("created_at")

    total_attempts = results.count()
    average_score = results.aggregate(avg=Avg("score"))["avg"] or 0

    topics_completed = (
        results.values("scenario__topic")
        .annotate(c=Count("scenario__topic", distinct=True))
        .count()
    )

    last_results = results.order_by("-created_at")[:10]

    chart_labels = [
        r.created_at.strftime("%d %b")
        for r in results
    ]

    chart_scores = [
        r.score for r in results
    ]

    plan = SubscriptionPlan.objects.get(is_active=True)
    return render(
        request,
        "dashboard.html",
        {
            "total_attempts": total_attempts,
            "average_score": round(average_score, 2),
            "topics_completed": topics_completed,
            "last_results": last_results,
            "chart_labels": chart_labels,
            "chart_scores": chart_scores,
            "plan": plan,
        }
    )
