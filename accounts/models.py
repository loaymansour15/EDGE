from django.conf import settings
from django.db import models
from django.utils import timezone

class ActiveSession(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    expires_at = models.DateTimeField()

    def is_active(self):
        return self.expires_at > timezone.now()
