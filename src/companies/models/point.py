from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel


class Point(TimestampedModel):
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="points",
    )
    address = models.CharField(
        _("point address"),
        max_length=255,
    )

    def __str__(self) -> str:
        return f"{self.company.name} - {self.address}"

    class Meta:
        verbose_name = _("point")
        verbose_name_plural = _("points")
