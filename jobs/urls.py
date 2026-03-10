from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import JobViewSet, WorkerBidListView

router = DefaultRouter()
router.register("jobs", JobViewSet, basename="jobs")

urlpatterns = router.urls
urlpatterns += [
    path("worker/bids/", WorkerBidListView.as_view(), name="worker-bids"),
]
