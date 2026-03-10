from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserStats, UserType


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile_number",
            "first_name",
            "last_name",
            "username",
            "display_name",
            "user_type",
            "is_online",
            "is_verified",
            "location",
            "portfolio_urls",
            "password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at", "updated_at"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_mobile_number(self, value):
        if User.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_user_type(self, value):
        if value not in [UserType.NORMAL_USER, UserType.GIG_WORKER]:
            raise serializers.ValidationError("Invalid user type.")
        return value

    def validate_portfolio_urls(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("portfolio_urls must be a list of URL strings.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile_number = serializers.CharField(required=False, max_length=20)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        mobile_number = attrs.get("mobile_number")
        password = attrs.get("password")

        if not email and not mobile_number:
            raise serializers.ValidationError("Provide email or mobile_number with password.")

        identifier = email or mobile_number
        user = authenticate(
            request=self.context.get("request"),
            username=identifier,
            password=password,
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        attrs["user"] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile_number = serializers.CharField(required=False, max_length=20)

    def validate(self, attrs):
        email = attrs.get("email")
        mobile_number = attrs.get("mobile_number")
        if not email and not mobile_number:
            raise serializers.ValidationError("Provide email or mobile_number.")

        user = User.objects.filter(email__iexact=email).first() if email else None
        if not user and mobile_number:
            user = User.objects.filter(mobile_number=mobile_number).first()
        attrs["user"] = user
        return attrs

    def build_reset_payload(self):
        """
        Placeholder flow.
        In production, send token via email/SMS instead of returning it.
        """
        user = self.validated_data["user"]
        if not user:
            return {
                "detail": "If an account exists for the provided identifier, a reset link has been sent."
            }

        token = PasswordResetTokenGenerator().make_token(user)
        return {
            "detail": "Password reset token generated.",
            "uid": str(user.id),
            "reset_token": token,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class UserStatsSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserStats
            fields = [
                "jobs_completed",
                "jobs_lost",
                "jobs_won",
                "profile_views",
                "rating",
            ]
            read_only_fields = fields

    stats = UserStatsSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile_number",
            "first_name",
            "last_name",
            "username",
            "display_name",
            "full_name",
            "user_type",
            "is_online",
            "is_verified",
            "location",
            "portfolio_urls",
            "stats",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class AuthResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserProfileSerializer()

    @staticmethod
    def build(user):
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserProfileSerializer(user).data,
        }
