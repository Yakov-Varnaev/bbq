from app.testing import register
from app.testing.factory import FixtureFactory
from users.types import RegistrationData, UserData


@register
def registration_data(self: FixtureFactory, **kwargs: RegistrationData) -> RegistrationData:
    schema = self.schema(
        schema=lambda: {
            "email": self.generic.person.email(),
            "first_name": self.generic.person.first_name(),
            "last_name": self.generic.person.last_name(),
            "password": self.generic.person.password(),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}  # type: ignore[typeddict-item]


@register
def expected_user_data(_: FixtureFactory, registration_data: RegistrationData) -> UserData:
    return {k: v for k, v in registration_data.items() if not k.startswith("password")}  # type: ignore[return-value]
