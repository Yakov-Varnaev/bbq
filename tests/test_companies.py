import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCRUD:

    def test_get(self, auth_setup):

        first_client, second_client = auth_setup

        assert first_client.get('/api/companies/').status_code == status.HTTP_200_OK
        assert second_client.get('/api/companies/').status_code == status.HTTP_200_OK
