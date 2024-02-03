from app.testing import register
from app.testing.types import FactoryProtocol
from companies.models import Point


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
