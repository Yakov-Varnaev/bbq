from app.testing import register
from app.testing.types import FactoryProtocol
from companies.models import Company, Point


@register
def company(self: FactoryProtocol, **kwargs: dict) -> Company:
    return self.mixer.blend(Company, **kwargs)


@register
def company_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"name": self.field("text.word")},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def company_point_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {
            "address": self.field("address"),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def company_point(self: FactoryProtocol, **kwargs: dict) -> Point:
    return self.mixer.blend(Point, **kwargs)
