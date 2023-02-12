from rest_framework import serializers

from .models import CompanyModel


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = '__all__'

    owner = serializers.ReadOnlyField(source='owner.id')
