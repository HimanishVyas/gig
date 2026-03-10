from rest_framework.permissions import BasePermission


class IsClientUser(BasePermission):
    """Allow only Normal Users (user_type == 1) to create jobs."""

    message = "Only client users can create job posts."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "user_type", None) == 1)


class IsWorkerUser(BasePermission):
    """Allow only Worker users (user_type == 2)."""

    message = "Only worker users can perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "user_type", None) == 2)


class IsJobOwner(BasePermission):
    """Allow only the job creator to view bids for their job."""

    message = "Only the job creator can view bids for this job."

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.created_by_id == request.user.id)
