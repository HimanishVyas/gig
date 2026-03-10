import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class BaseModel(models.Model):
    """Reusable abstract base with UUID and audit timestamps."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.IntegerChoices):
    NORMAL_USER = 1, "Normal User"
    GIG_WORKER = 2, "Gig Worker"


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    user_type = models.PositiveSmallIntegerField(
        choices=UserType.choices,
        default=UserType.NORMAL_USER,
    )
    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True)
    # Stored as ["https://...", "https://..."].
    portfolio_urls = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile_number", "username"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["mobile_number"]),
            models.Index(fields=["username"]),
            models.Index(fields=["user_type"]),
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.full_name} <{self.email}>"


class UserStats(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    jobs_completed = models.PositiveIntegerField(default=0)
    jobs_lost = models.PositiveIntegerField(default=0)
    jobs_won = models.PositiveIntegerField(default=0)
    profile_views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    class Meta:
        db_table = "user_stats"

    def __str__(self):
        return f"Stats<{self.user_id}>"


class CountryMaster(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = "country_master"
        verbose_name_plural = "Country Master"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class StateMaster(BaseModel):
    country = models.ForeignKey(
        CountryMaster,
        on_delete=models.CASCADE,
        related_name="states",
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "state_master"
        unique_together = ("country", "name")
        ordering = ["country__name", "name"]

    def __str__(self):
        return f"{self.name} - {self.country.code}"


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    state = models.ForeignKey(StateMaster, on_delete=models.PROTECT, related_name="addresses")
    country = models.ForeignKey(CountryMaster, on_delete=models.PROTECT, related_name="addresses")

    class Meta:
        db_table = "address"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.city}"
