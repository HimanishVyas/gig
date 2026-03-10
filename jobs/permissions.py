from rest_framework.permissions import BasePermission


class IsClientUser(BasePermission):
    """Allow only Normal Users (user_type == 1) to create jobs."""

    message = "Only client users can create job posts."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "user_type", None) == 1)
