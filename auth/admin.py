from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Address, CountryMaster, StateMaster, User, UserStats


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "mobile_number",
        "first_name",
        "last_name",
        "username",
        "user_type",
        "is_online",
        "is_verified",
        "is_active",
        "is_staff",
        "created_at",
    )
    search_fields = ("email", "mobile_number", "first_name", "last_name", "username")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "mobile_number", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "display_name",
                    "location",
                    "portfolio_urls",
                    "user_type",
                    "is_online",
                    "is_verified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "last_login")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "mobile_number",
                    "first_name",
                    "last_name",
                    "username",
                    "display_name",
                    "user_type",
                    "is_online",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "jobs_completed", "jobs_lost", "jobs_won", "profile_views", "rating")
    search_fields = ("user__email", "user__username")


@admin.register(CountryMaster)
class CountryMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")
    search_fields = ("name", "code")


@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "country", "created_at")
    search_fields = ("name", "code", "country__name")
    list_filter = ("country",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "line_1", "city", "zipcode", "state", "country", "created_at")
    search_fields = ("user__email", "user__username", "city", "zipcode")
    list_filter = ("country", "state")
