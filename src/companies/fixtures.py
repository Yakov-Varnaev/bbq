import pytest

from mixer.backend.django import mixer as _mixer

from app.testing import ApiClient
from companies.models import Company
from users.models import User


@pytest.fixture
def company() -> Company:
    return _mixer.blend("companies.Company")


@pytest.fixture
def company_owner(company: Company) -> User:
    return company.owner


@pytest.fixture
def owner_client(company_owner: User) -> ApiClient:
    return ApiClient(company_owner)


# Register your project-wide fixtures here.
# Add this file to root conftest pytest_plugins.
