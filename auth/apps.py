from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # Keep module name as "auth" (as requested) but avoid app-label conflict
    # with django.contrib.auth.
    name = "auth"
    label = "users_auth"
    verbose_name = "User Authentication"
