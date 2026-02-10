from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.views import LoginView

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from .models import ActiveSession

from django.contrib.auth.forms import AuthenticationForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm



def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    error = None

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        try:
            secure_login(request, user)
            return redirect("/dashboard/")
        except Exception as e:
            if str(e) == "ACCOUNT_ALREADY_LOGGED_IN":
                error = "الحساب مفتوح بالفعل من جهاز آخر"
            else:
                error = "حصل خطأ غير متوقع"

    return render(request, "login.html", {
        "form": form,
        "error": error
    })


SESSION_DURATION = timedelta(hours=1)

def secure_login(request, user):
    active_session = ActiveSession.objects.filter(user=user).first()

    # لو في سيشن نشطة → ارفض
    if active_session and active_session.is_active():
        raise Exception("ACCOUNT_ALREADY_LOGGED_IN")

    # Login طبيعي
    login(request, user)

    # خزّن السيشن الجديدة
    ActiveSession.objects.update_or_create(
        user=user,
        defaults={
            "session_key": request.session.session_key,
            "expires_at": timezone.now() + SESSION_DURATION
        }
    )


def logout_view(request):
    ActiveSession.objects.filter(user=request.user).delete()
    logout(request)
    return redirect("/login/")


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("/topics-page/")
    return render(request, "landing.html")

