import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from companies.models import Company, CompanyPoint, Department, Employee

User = get_user_model()


@pytest.fixture
def company(user):
    return mixer.blend(Company, owner=user)


@pytest.fixture
def company_point(company):
    return mixer.blend(CompanyPoint, company=company)


@pytest.fixture
def employee(company_point):
    return mixer.blend(Employee, point=company_point)


@pytest.fixture
def department(company_point):
    return mixer.blend(Department, point=company_point)


@pytest.fixture
def companies(user):
    return mixer.cycle(5).blend(Company, owner=user)
