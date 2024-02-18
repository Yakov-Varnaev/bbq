from typing import Self

from django.db import models

from app.models import ArchiveDeletedManager, ArchiveDeletedQuerySet


class _MaterialQuerySet(ArchiveDeletedQuerySet):
    def with_material_info(self) -> Self:
        return self.annotate(
            name=models.F("material__material__name"),
            brand=models.F("material__material__brand"),
            kind=models.F("material__material__kind"),
            unit=models.F("material__material__unit"),
        )

    def point(self, company_id: int, point_id: int) -> Self:
        return self.filter(
            material__stock__point__company_id=company_id,
            material__stock__point_id=point_id,
        )


class _MaterialManager(ArchiveDeletedManager):
    def get_queryset(self) -> _MaterialQuerySet:
        return _MaterialQuerySet(self.model, using=self._db).not_archived()

    def with_material_info(self) -> _MaterialQuerySet:
        return self.get_queryset().with_material_info()

    def point(self, company_id: int, point_id: int) -> _MaterialQuerySet:
        return self.get_queryset().point(company_id, point_id)
