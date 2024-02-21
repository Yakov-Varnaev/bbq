from rest_framework import serializers

from purchases.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("id", "created", "is_paid_by_card")
        read_only_fields = ("id", "created")
