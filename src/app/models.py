from typing import Any, Self

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

__all__ = [
    "models",
    "DefaultModel",
    "TimestampedModel",
    "ArchiveDeleted",
    "ArchiveDeletedQuerySet",
    "ArchiveDeletedManager",
]


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Default name for all models"""
        name = getattr(self, "name", None)
        if name is not None:
            return str(name)

        return super().__str__()

    @classmethod
    def get_contenttype(cls) -> ContentType:
        return ContentType.objects.get_for_model(cls)

    def update_from_kwargs(self, **kwargs: dict[str, Any]) -> None:
        """A shortcut method to update model instance from the kwargs."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def setattr_and_save(self, key: str, value: Any) -> None:
        """Shortcut for testing -- set attribute of the model and save"""
        setattr(self, key, value)
        self.save()

    @classmethod
    def get_label(cls) -> str:
        """Get a unique within the app model label"""
        return cls._meta.label_lower.split(".")[-1]


class TimestampedModel(DefaultModel):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class ArchiveDeletedQuerySet(models.QuerySet):
    def not_archived(self) -> Self:
        return self.filter(deleted__isnull=True)

    def archived(self) -> Self:
        return self.filter(deleted__isnull=False)


class ArchiveDeletedManager(models.Manager):
    def get_queryset(self) -> ArchiveDeletedQuerySet:
        return ArchiveDeletedQuerySet(self.model, using=self._db).not_archived()


class ArchiveDeleted(DefaultModel):
    archived = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    objects = ArchiveDeletedManager()
    include_archived = ArchiveDeletedQuerySet.as_manager()

    def __check_object_exists(self) -> None:
        if not self.pk:
            raise ObjectDoesNotExist("Object must be created before this operation.")

    def delete(self, *args: Any, **kwargs: Any) -> Self:
        self.__check_object_exists()
        self.archived = timezone.now()
        return super(ArchiveDeleted, self).save(*args, **kwargs)

    def restore(self, *args: Any, **kwargs: Any) -> Self:
        self.__check_object_exists()
        self.archived = None
        return super(ArchiveDeleted, self).save(*args, **kwargs)
