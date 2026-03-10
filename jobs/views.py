from rest_framework import mixins, permissions, viewsets

from .models import Job, JobStatus
from .permissions import IsClientUser
from .serializers import JobSerializer


class JobViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    - Create: only Normal Users (clients).
    - List/Retrieve: only OPEN jobs, newest first.
    """

    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(status=JobStatus.OPEN).order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsClientUser()]
        return [permissions.IsAuthenticated()]
