import hashlib
import unicodedata

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Authenticate Django users by email instead of their internal username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = (username or kwargs.get("email") or "").strip()
        if not email or password is None:
            return None

        user_model = get_user_model()
        try:
            user = user_model.objects.get(email__iexact=email)
        except user_model.DoesNotExist:
            # Perform a password hash to reduce timing differences for unknown emails.
            user_model().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


def username_for_email(email):
    """Return a stable username within Django's 150-character limit."""
    normalized_email = email.strip().lower()
    suffix = hashlib.sha256(unicodedata.normalize("NFKC", normalized_email).encode("utf-8")).hexdigest()[:20]
    return f"{normalized_email[:120]}-{suffix}"
