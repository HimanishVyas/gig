from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class EmailOrMobileBackend(ModelBackend):
    """Authenticate users using either email or mobile_number."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = kwargs.get("email") or kwargs.get("mobile_number") or username
        if not identifier or not password:
            return None

        try:
            user = User.objects.get(Q(email__iexact=identifier) | Q(mobile_number=identifier))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
