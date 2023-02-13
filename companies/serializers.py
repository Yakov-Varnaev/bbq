from rest_framework import serializers
from djoser.serializers import UserSerializer

from .models import Company, CompanyPoint, Employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    owner = serializers.ReadOnlyField(source='owner.id')


class CompanyPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPoint
        fields = '__all__'


class CompanyPointDetailSerializer(CompanyPointSerializer):
    company = CompanySerializer()


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeDetailSerializer(EmployeeSerializer):
    user = UserSerializer()
    point = CompanyPointDetailSerializer()
