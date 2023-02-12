import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCRUD:

    def test_get(self, auth_setup):

        client = auth_setup[0]

        assert client.get('/api/companies/').status_code == status.HTTP_200_OK

    def test_post(self, auth_setup):

        client = auth_setup[0]
        post_data = {'name': 'TestCompany'}

        response = client.post('/api/companies/', data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_put(self, auth_setup):

        first_client, second_client = auth_setup

        post_data = {'name': 'TestCompany'}
        put_data = {'name': 'TestCompany2'}

        response = first_client.post('/api/companies/', data=post_data)
        company_id = response.data['id']

        company_uri = f'/api/companies/{company_id}/'

        assert first_client.put(company_uri, data=put_data).status_code == status.HTTP_200_OK
        assert second_client.put(company_uri, data=put_data).status_code != status.HTTP_200_OK

    def test_delete(self, auth_setup):

        first_client, second_client = auth_setup

        post_data = {'name': 'TestCompany'}

        response = first_client.post('/api/companies/', data=post_data)
        company_id = response.data['id']

        company_uri = f'/api/companies/{company_id}/'

        assert second_client.delete(company_uri).status_code != status.HTTP_204_NO_CONTENT
        assert first_client.delete(company_uri).status_code == status.HTTP_204_NO_CONTENT
