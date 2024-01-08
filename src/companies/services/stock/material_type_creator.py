from typing import Callable

from rest_framework.serializers import BaseSerializer

from app.services import BaseService
from companies.api.serializers import MaterialTypeSerializer


class MaterialTypeCreator(BaseService):
    def __init__(self, serializer: BaseSerializer[MaterialTypeSerializer]) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def act(self) -> None:
        self.serializer.save()  # TODO get_or_create  # noqa:  T101
