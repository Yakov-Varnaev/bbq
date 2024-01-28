from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import DefaultModel


class Department(models.Model):
    point = models.ForeignKey(
        "companies.Point", on_delete=models.CASCADE, related_name="departments", verbose_name=_("point")
    )
    name = models.CharField(_("department name"), max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = _("department")
        verbose_name_plural = _("departments")


class Category(DefaultModel):
    name = models.CharField(
        _("procedure category name"),
        max_length=255,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("procedure category")
        verbose_name_plural = _("categories of procedures")


class Procedure(DefaultModel):
    name = models.CharField(_("procedure name"), max_length=255)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="procedures", verbose_name=_("procedure category")
    )
    department = models.ForeignKey(
        "Department", on_delete=models.CASCADE, related_name="procedures", verbose_name=_("department")
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("procedure")
        verbose_name_plural = _("procedures")

    def get_absolute_url(self) -> str:
        from django.urls import reverse
        return reverse(  # noqa: BLK100
            "api_v1:companies:procedure-detail",
            kwargs={
                "company_pk": self.department.point.company.id,
                "point_pk": self.department.point.id,
                "department_pk": self.department.id,
                "pk": self.pk,
            },
        )
