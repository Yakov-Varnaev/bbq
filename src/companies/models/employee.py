from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeleted, TimestampedModel


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
        ordering = ("fire_date",)
        verbose_name = _("employee")
        verbose_name_plural = _("employees")


class MasterProcedure(TimestampedModel, ArchiveDeleted):
    procedure = models.ForeignKey(
        "companies.Procedure",
        on_delete=models.PROTECT,
        related_name="procedures",
    )
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.PROTECT,
        related_name="employees",
    )
    price = models.PositiveIntegerField(_("procedure price"))
    coef = models.FloatField(
        _("coefficient"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    class Meta:
        ordering = ("employee", "procedure")
        verbose_name = _("procedure master")
        verbose_name_plural = _("procedure masters")

    def get_absolute_url(self) -> str:
        return reverse(
            "api_v1:companies:master-procedure-detail",
            kwargs={
                "company_pk": self.procedure.department.point.company.id,
                "point_pk": self.procedure.department.point.id,
                "employee_pk": self.employee.id,
                "pk": self.id,
            },
        )
