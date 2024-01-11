import logging
from typing import Callable

from rest_framework.serializers import BaseSerializer

from app.services import BaseService
from companies.api.serializers import MaterialTypeSerializer
from companies.models import MaterialType


class MaterialTypeCreator(BaseService):
    def __init__(self, serializer: BaseSerializer[MaterialTypeSerializer]) -> None:
        self.serializer = serializer
        self.logger = logging.getLogger(__name__)

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def act(self) -> MaterialType:
        material_type, created = MaterialType.objects.get_or_create(name=self.serializer.validated_data["name"])
        if created:
            self.logger.info("MaterialType with name `%s` was created.", material_type.name)
        else:
            self.logger.info("MaterialType with name `%s` already exists.", material_type.name)
        return material_type
