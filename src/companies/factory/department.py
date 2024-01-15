from app.testing import register
from app.testing.types import FactoryProtocol
from companies.models import Department, Procedure


@register
def department_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"name": self.field("text.word")},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def department(self: FactoryProtocol, **kwargs: dict) -> Department:
    return self.mixer.blend(Department, **kwargs)


@register
def procedure_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"name": self.field("text.word")},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def procedure(self: FactoryProtocol, **kwargs: dict) -> Procedure:
    return self.mixer.blend(Procedure, **kwargs)
