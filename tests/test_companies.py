import pytest
from rest_framework import status

from companies.models import Company
from companies.serializers import CompanySerializer
from utils.tests.mixins import TestUtils


@pytest.mark.django_db
class TestCRUD(TestUtils):
    model_class = Company
    base_url_name = 'companies'

    def test_retrieve(self, company, auth_client):
        response = auth_client.get(self.detail_url(company.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == CompanySerializer(company).data

    def test_list(self, companies, auth_client):
        response = auth_client.get(self.list_url())

        assert response.status_code == status.HTTP_200_OK
        assert response.data == CompanySerializer(companies, many=True).data

    def test_post(self, user, auth_client):
        data = {'name': 'TestCompany'}
        count = self.get_count()
        response = auth_client.post(self.list_url(), data=data)
        company = self.retrieve()

        assert self.get_count() == count + 1, 'Company was not created.'
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == CompanySerializer(company).data
        assert company.owner == user

    def test_put(self, company, auth_client):
        put_data = {'name': 'TestCompany'}
        count = self.get_count()
        response = auth_client.put(self.detail_url(company.id), data=put_data)
        upd_company = self.retrieve()

        assert self.get_count() == count, 'New company was create on update.'
        assert response.status_code == status.HTTP_200_OK
        assert response.data == CompanySerializer(upd_company).data
        assert (
            upd_company.time_updated > company.time_updated
        ), 'Updated time was not updated on update.'

    def test_delete(self, company, auth_client):
        count = self.get_count()
        response = auth_client.delete(self.detail_url(company.id))

        assert self.get_count() == count - 1, 'Company was not deleted'
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Company.objects.filter(id=company.id).exists()

    def test_delete_non_owner(self, company, auth_another_client):
        client = auth_another_client
        count = self.get_count()
        response = client.delete(self.detail_url(company.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.get_count() == count
        assert Company.objects.filter(id=company.id).exists()

    def test_update_non_owner(self, company, auth_another_client):
        client = auth_another_client
        count = self.get_count()
        response = client.delete(self.detail_url(company.id), data={'name': f'new {company.name}'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.get_count() == count
        assert self.retrieve().time_updated == company.time_updated
        assert Company.objects.filter(id=company.id, name=company.name).exists()
