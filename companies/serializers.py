from rest_framework import serializers

from .models import Company, CompanyPoint


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
