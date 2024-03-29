from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel

User = get_user_model()


class Company(TimestampedModel):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = _("company")
        verbose_name_plural = _("companies")
