import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCRUD:

    def test_get(self, auth_setup):

        client = auth_setup[0]

        assert client.get('/api/companies/').status_code == status.HTTP_200_OK

    def test_post(self, auth_setup):

        client = auth_setup[0]
        post_data = {'name': 'TestCompany', 'owner': 1}

        response = client.post('/api/companies/', data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_put(self, auth_setup):

        first_client, second_client = auth_setup

        post_data = {'name': 'TestCompany', 'owner': 1}
        put_data = {'name': 'TestCompany2', 'owner': 1}

        first_client.post('/api/companies/', data=post_data)

        assert first_client.put('/api/companies/1/', data=put_data).status_code == status.HTTP_200_OK
        assert second_client.put('/api/companies/1/', data=put_data).status_code != status.HTTP_200_OK

    def test_delete(self, auth_setup):

        first_client, second_client = auth_setup

        post_data = {'name': 'TestCompany', 'owner': 1}

        first_client.post('/api/companies/', data=post_data)

        assert second_client.delete('/api/companies/1/').status_code != status.HTTP_204_NO_CONTENT
        assert first_client.delete('/api/companies/1/').status_code == status.HTTP_204_NO_CONTENT
