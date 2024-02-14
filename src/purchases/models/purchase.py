from typing import Self

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedCreatedModel


class PurchaseQuerySet(models.QuerySet):
    def point(self, company_id: int, point_id: int) -> Self:
        return self.filter(
            id__procedure__department__point__company_id=company_id,
            id__procedure__department__point_id=point_id,
        )


class PurchaseManager(models.Manager):
    def get_queryset(self) -> PurchaseQuerySet:
        return PurchaseQuerySet(self.model, using=self._db)

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
        return f"Payment by {'card' if self.is_paid_by_card else 'cash'} at {self.created}"
