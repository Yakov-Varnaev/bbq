from app.testing import register
from app.testing.types import FactoryProtocol
from companies.models.department import Department


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
