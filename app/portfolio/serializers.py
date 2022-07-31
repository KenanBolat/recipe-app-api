"""
Serializers for Portfolio API.
"""
from rest_framework import serializers

from core.models import (Portfolio)


class PortfolioSerializers(serializers.ModelSerializer):
    """Serializer for """

    class Meta:
        model = Portfolio
        fields = ['id', 'name']
        read_only_fields = ['id']


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for portfolio."""
    class Meta:
        model = Portfolio
        fields = ['id',
                  'title',
                  'link', ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a portfolio."""
        portfolio = Portfolio.objects.create(**validated_data)
        return portfolio

    def update(self, instance, validated_data):
        """Update portfolio."""

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PortfolioDetailSerializer(PortfolioSerializer):
    """Serializer for portfolio detail view."""

    class Meta(PortfolioSerializer.Meta):
        fields = PortfolioSerializer.Meta.fields + ['description']
