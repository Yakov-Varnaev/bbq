from typing import Callable

from app.services import BaseService
from companies.api.serializers.employee import EmployeeSerializer
from companies.models import Employee


class EmployeeCreator(BaseService):
    def __init__(self, serializer: EmployeeSerializer) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def act(self) -> Employee:
        return self.serializer.save()
