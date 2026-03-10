from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import JobFilter
from .models import Bid, Job, JobStatus
from .permissions import IsClientUser, IsJobOwner, IsWorkerUser
from .serializers import BidListSerializer, BidSerializer, JobSerializer, WorkerBidSerializer


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Job.objects.filter(status=JobStatus.OPEN).order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsClientUser()]
        if self.action == "bid":
            return [permissions.IsAuthenticated(), IsWorkerUser()]
        if self.action == "bids":
            return [permissions.IsAuthenticated(), IsJobOwner()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=["post"], url_path="bid")
    def bid(self, request, pk=None):
        job = self.get_object()
        serializer = BidSerializer(data=request.data, context={"request": request, "job": job})
        serializer.is_valid(raise_exception=True)
        bid = serializer.save()
        return Response(BidListSerializer(bid).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="bids")
    def bids(self, request, pk=None):
        job = self.get_object()
        self.check_object_permissions(request, job)
        qs = Bid.objects.filter(job=job).order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = BidListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(BidListSerializer(qs, many=True).data, status=status.HTTP_200_OK)


class WorkerBidListView(APIView, PageNumberPagination):
    permission_classes = [permissions.IsAuthenticated, IsWorkerUser]

    def get(self, request, *args, **kwargs):
        qs = Bid.objects.filter(worker=request.user).order_by("-created_at")
        page = self.paginate_queryset(qs, request, view=self)
        if page is not None:
            serializer = WorkerBidSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(WorkerBidSerializer(qs, many=True).data, status=status.HTTP_200_OK)
