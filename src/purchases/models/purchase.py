from typing import Self

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeletedManager, ArchiveDeletedQuerySet, TimestampedCreatedModel


class PurchaseQuerySet(ArchiveDeletedQuerySet):
    def point(self, company_id: int, point_id: int) -> Self:
        return self.filter(
            procedure__department__point__company_id=company_id,
            procedure__department__point_id=point_id,
        )


class PurchaseManager(ArchiveDeletedManager):
    def get_queryset(self) -> PurchaseQuerySet:
        return PurchaseQuerySet(self.model, using=self._db).not_archived()

    def point(self, company_id: int, point_id: int) -> PurchaseQuerySet:
        return self.get_queryset().point(company_id, point_id)


class Purchase(TimestampedCreatedModel):
    is_paid_by_card = models.BooleanField(_("paid by card"))

    objects = PurchaseManager()
    include_archived = PurchaseQuerySet.as_manager()

    class Meta:
        verbose_name = _("purchase")
        verbose_name_plural = _("purchases")
        ordering = ("created",)

    def __str__(self) -> str:
        return f"Buying {self.procedure.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            "api_v1:purchases:purchase-detail",
            kwargs={
                "company_pk": self.procedure.department.point.company.pk,
                "point_pk": self.procedure.department.point.pk,
                "pk": self.pk,
            },
        )
