from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Custom manager for User model."""

    use_in_migrations = True

    def _create_user(self, email, mobile_number, password, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        if not mobile_number:
            raise ValueError("Mobile number is required.")
        if not extra_fields.get("username"):
            raise ValueError("Username is required.")
        if not password:
            raise ValueError("Password is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)  # Uses Django's secure password hashing.
        user.save(using=self._db)
        return user

    def create_user(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, mobile_number, password, **extra_fields)

    def create_superuser(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, mobile_number, password, **extra_fields)
