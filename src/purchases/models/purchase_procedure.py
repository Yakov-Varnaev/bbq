from typing import Self

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeleted, ArchiveDeletedManager, ArchiveDeletedQuerySet


class PurchaseProcedureQuerySet(ArchiveDeletedQuerySet):
    def point(self, company_id: int, point_id: int) -> Self:
        return self.filter(
            procedure__department__point__company_id=company_id,
            procedure__department__point_id=point_id,
        )


class PurchaseProcedureManager(ArchiveDeletedManager):
    def get_queryset(self) -> PurchaseProcedureQuerySet:
        return PurchaseProcedureQuerySet(self.model, using=self._db).not_archived()

    def point(self, company_id: int, point_id: int) -> PurchaseProcedureQuerySet:
        return self.get_queryset().point(company_id, point_id)


class PurchaseProcedure(ArchiveDeleted):
    purchase = models.ForeignKey(
        "purchases.Purchase",
        on_delete=models.PROTECT,
        related_name="purchase_procedures",
    )
    procedure = models.ForeignKey(
        "companies.Procedure",
        on_delete=models.PROTECT,
        related_name="purchase_procedures",
    )

    objects = PurchaseProcedureManager()
    include_archived = PurchaseProcedureQuerySet.as_manager()

    class Meta:
        verbose_name = _("purchase of procedure")
        verbose_name_plural = _("purchase of procedures")
        ordering = ("purchase", "procedure")

    def __str__(self) -> str:
        return f"Purchase {self.procedure.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            "api_v1:purchases:procedures-purchase-detail",
            kwargs={
                "company_pk": self.procedure.department.point.company.pk,
                "point_pk": self.procedure.department.point.pk,
                "pk": self.pk,
            },
        )
