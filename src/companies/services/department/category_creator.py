import logging
from typing import Callable

from rest_framework.serializers import BaseSerializer

from app.services import BaseService
from companies.api.serializers import CategorySerializer
from companies.models import Category

logger = logging.getLogger(__name__)


class CategoryCreator(BaseService):
    def __init__(self, serializer: BaseSerializer[CategorySerializer]) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def act(self) -> Category:
        category, created = Category.objects.get_or_create(name=self.serializer.validated_data["name"])
        msg = "Category with name `%s` was created." if created else "Category with name `%s` already exists."
        logger.info(msg, category.name)
        return category
