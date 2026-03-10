from django.contrib import admin

from .models import Bid, Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "location",
        "status",
        "created_by",
        "created_at",
    )
    search_fields = ("title", "category", "location", "created_by__email")
    list_filter = ("status", "category")
    ordering = ("-created_at",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "worker",
        "bid_price",
        "estimated_days",
        "status",
        "created_at",
    )
    search_fields = ("job__title", "worker__email", "worker__username")
    list_filter = ("status",)
    ordering = ("-created_at",)
