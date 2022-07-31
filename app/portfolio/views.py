"""
Views for the portfolio APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from rest_framework import (viewsets, mixins, status)
# mixins is required to add additional functionalities to views

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Portfolio, Tag)

from . import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma seperated list of tag IDs to filter',
            )
        ]
    )
)
class PortfolioViewSet(viewsets.ModelViewSet):
    """View from the manage portfolio APIs."""
    serializer_class = serializers.PortfolioDetailSerializer
    queryset = Portfolio.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        # 1,2,3
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve portfolios for authenticated user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PortfolioSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """create a new portfolio."""
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to portfolios.'
            )
        ]
    )
)
class BasePortfolioAttrViewSet(mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Base Portfolio Attribute for View Sets"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(portfolio__isnull=False)
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BasePortfolioAttrViewSet):
    """Manage Tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
