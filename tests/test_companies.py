import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCRUD:

    def test_get(self, auth_client):
        assert auth_client.get('/api/companies/').status_code == status.HTTP_200_OK

    def test_post(self, auth_client):
        post_data = {'name': 'TestCompany'}
        response = auth_client.post('/api/companies/', data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_put(self, company, auth_client, auth_unauthorized_client):
        put_data = {'name': 'TestCompany2'}
        company_uri = f'/api/companies/{company.id}/'

        assert auth_client.put(company_uri, data=put_data).status_code == status.HTTP_200_OK
        assert auth_unauthorized_client.put(company_uri, data=put_data).status_code != status.HTTP_200_OK

    def test_delete(self, company, auth_client, auth_unauthorized_client):
        company_uri = f'/api/companies/{company.id}/'

        assert auth_unauthorized_client.delete(company_uri).status_code != status.HTTP_204_NO_CONTENT
        assert auth_client.delete(company_uri).status_code == status.HTTP_204_NO_CONTENT
