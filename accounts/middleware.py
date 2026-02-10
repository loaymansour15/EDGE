from django.shortcuts import redirect
from django.utils import timezone
from .models import ActiveSession

class EnforceSingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ حماية إضافية
        if not hasattr(request, "user"):
            return self.get_response(request)
        
        if request.user.is_authenticated:
            session = ActiveSession.objects.filter(user=request.user).first()

            if not session or session.expires_at < timezone.now():
                ActiveSession.objects.filter(user=request.user).delete()
                from django.contrib.auth import logout
                logout(request)
                return redirect("/login/?expired=1")

        return self.get_response(request)
