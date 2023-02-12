from rest_framework import serializers

from .models import CompaniesModel


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompaniesModel
        fields = '__all__'

    owner = serializers.ReadOnlyField(source='owner.id')
