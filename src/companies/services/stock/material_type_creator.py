import logging
from typing import Callable

from rest_framework.serializers import BaseSerializer

from app.services import BaseService
from companies.api.serializers import MaterialTypeSerializer
from companies.models import MaterialType

logger = logging.getLogger(__name__)


class MaterialTypeCreator(BaseService):
    def __init__(self, serializer: BaseSerializer[MaterialTypeSerializer]) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def act(self) -> MaterialType:
        material_type, created = MaterialType.objects.get_or_create(name=self.serializer.validated_data["name"])
        msg = "MaterialType with name `%s` was created." if created else "MaterialType with name `%s` already exists."
        logger.info(msg, material_type.name)
        return material_type
