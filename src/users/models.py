from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseDjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseDjangoUserManager):
    def __perform_create(self, email: str, password: str, **extra_fields: dict) -> "User":
        if not email:
            raise ValueError(_("The given email must be set"))
        extra_fields.pop("username", None)

        email = self.normalize_email(email)
        username = email.replace("@", "_").replace(".", "_")
        return self._create_user(username, email, password, **extra_fields)  # type: ignore[attr-defined]

    def create_user(self, email: str, password: str, **extra_fields: dict) -> "User":  # type: ignore[override]
        extra_fields.setdefault("is_staff", False)  # type: ignore[arg-type]
        extra_fields.setdefault("is_superuser", False)  # type: ignore[arg-type]
        return self.__perform_create(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> "User":  # type: ignore[override]
        extra_fields.setdefault("is_staff", True)  # type: ignore[arg-type]
        extra_fields.setdefault("is_superuser", True)  # type: ignore[arg-type]
        return self.__perform_create(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()  # type: ignore

    email = models.EmailField(_("email"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.get_full_name()}({self.email})"
