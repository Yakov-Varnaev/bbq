from typing import Self

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeleted, ArchiveDeletedManager, ArchiveDeletedQuerySet, TimestampedCreatedModel


class PurchaseQuerySet(ArchiveDeletedQuerySet):
    def point(self, company_id: int, point_id: int) -> Self:
        return self.filter(
            purchase_procedures__procedure__department__point__company_id=company_id,
            purchase_procedures__procedure__department__point_id=point_id,
        )


class PurchaseManager(ArchiveDeletedManager):
    def get_queryset(self) -> PurchaseQuerySet:
        return PurchaseQuerySet(self.model, using=self._db).not_archived()

    def point(self, company_id: int, point_id: int) -> PurchaseQuerySet:
        return self.get_queryset().point(company_id, point_id)


class Purchase(ArchiveDeleted, TimestampedCreatedModel):
    is_paid_by_card = models.BooleanField(_("paid by card"))

    objects = PurchaseManager()
    include_archived = PurchaseQuerySet.as_manager()

    class Meta:
        verbose_name = _("purchase")
        verbose_name_plural = _("purchases")
        ordering = ("created",)

    def __str__(self) -> str:
        return f"Payment by {'card' if self.is_paid_by_card else 'cash'} at {self.created}"
