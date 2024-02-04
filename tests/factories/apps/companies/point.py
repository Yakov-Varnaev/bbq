from app.testing import register
from app.testing.factory import FixtureFactory
from companies.models import Point


@register
def company_point_data(self: FixtureFactory, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {
            "address": self.field("address"),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def company_point(self: FixtureFactory, **kwargs: dict) -> Point:
    return self.mixer.blend(Point, **kwargs)
