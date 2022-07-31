"""
Serializers for Portfolio API.
"""
from rest_framework import serializers

from core.models import (Portfolio, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Serializers for Tag."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class PortfolioSerializers(serializers.ModelSerializer):
    """Serializer for """

    class Meta:
        model = Portfolio
        fields = ['id', 'name']
        read_only_fields = ['id']


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for portfolio."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Portfolio
        fields = ['id',
                  'title',
                  'link',
                  'tags',]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, portfolio):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, create = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            portfolio.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a portfolio."""
        tags = validated_data.pop('tags', [])
        portfolio = Portfolio.objects.create(**validated_data)
        self._get_or_create_tags(tags=tags, portfolio=portfolio)
        return portfolio

    def update(self, instance, validated_data):
        """Update portfolio."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PortfolioDetailSerializer(PortfolioSerializer):
    """Serializer for portfolio detail view."""

    class Meta(PortfolioSerializer.Meta):
        fields = PortfolioSerializer.Meta.fields + ['description']

