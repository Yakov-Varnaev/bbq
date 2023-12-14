from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel


class Employee(TimestampedModel):
    departments = models.ManyToManyField(
        "companies.Department",
        related_name="employees",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="employees",
    )
    position = models.CharField(
        _("employee position"),
        max_length=255,
    )
    fire_date = models.DateField(
        _("employee fire date"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
