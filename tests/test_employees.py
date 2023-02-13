import pytest
from rest_framework import status
from companies.models import Employee
from companies.serializers import EmployeeDetailSerializer, EmployeeSerializer
from utils.tests.mixins import TestUtils


@pytest.mark.django_db
class TestEmployees(TestUtils):
    model_class = Employee
    base_url_name = 'employees'

    def test_owner_can_create_employee(self, company_point, auth_client, another_user):
        count = self.get_count()
        data = {'position': 'CTO', 'user': another_user.id, 'point': company_point.id}
        response = auth_client.post(
            self.list_url(company_point.company.id, company_point.id), data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.get_count() == count + 1
        assert response.data == EmployeeSerializer(self.retrieve()).data

    def test_non_owner_cannot_create_employee(
        self, user_factory, company_point, auth_another_client
    ):
        count = self.get_count()
        user = user_factory()
        data = {'position': 'CTO', 'user': user.id, 'point': company_point.id}
        response = auth_another_client.post(
            self.list_url(company_point.company.id, company_point.id), data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.get_count() == count
        assert not Employee.objects.filter(point=company_point, user=user).exists()

    def test_retrieve(self, employee, client):
        response = client.get(
            self.detail_url(employee.point.company.id, employee.point.id, employee.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == EmployeeDetailSerializer(self.retrieve()).data

    def test_list(self, employee, client):
        response = client.get(self.list_url(employee.point.company.id, employee.point.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == EmployeeSerializer(self.filter(), many=True).data

    def test_owner_can_update(self, employee, auth_client):
        count = self.get_count()
        data = EmployeeSerializer(employee).data
        data['position'] = 'CTO'
        data.pop('fired')
        response = auth_client.put(
            self.detail_url(employee.point.company.id, employee.point.id, employee.id), data=data
        )
        empl = self.retrieve()

        assert response.status_code == status.HTTP_200_OK, response.data
        assert self.get_count() == count
        assert response.data == EmployeeSerializer(empl).data
        assert empl.position == data['position']

    def test_non_owner_cannot_update(self, employee, auth_another_client):
        count = self.get_count()
        data = EmployeeSerializer(employee).data
        data['position'] = 'CTO'
        data.pop('fired')
        response = auth_another_client.put(
            self.detail_url(employee.point.company.id, employee.point.id, employee.id), data=data
        )
        empl = self.retrieve()

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.data
        assert self.get_count() == count
        assert empl.position == employee.position

    def test_owner_can_delete(self, employee, auth_client):
        count = self.get_count()
        response = auth_client.delete(
            self.detail_url(employee.point.company.id, employee.point.id, employee.id)
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.get_count() == count - 1

    def test_non_owner_cannot_delete(self, employee, auth_another_client):
        count = self.get_count()
        response = auth_another_client.delete(
            self.detail_url(employee.point.company.id, employee.point.id, employee.id)
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.get_count() == count
