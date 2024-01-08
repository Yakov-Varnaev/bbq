from typing import Callable

from app.services import BaseService
from companies.api.serializers import MaterialTypeSerializer
from companies.models import MaterialType


class MaterialTypeCreator(BaseService):
    def __init__(self, serializer: MaterialTypeSerializer) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def act(self) -> MaterialType:
        return self.serializer.save()  # TODO get_or_create  # noqa:  T101
