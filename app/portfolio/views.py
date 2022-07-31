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

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Portfolio)

from . import serializers


class PortfolioViewSet(viewsets.ModelViewSet):
    """View from the manage portfolio APIs."""
    serializer_class = serializers.PortfolioDetailSerializer
    queryset = Portfolio.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """Retrieve portfolios for authenticated user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        queryset = self.queryset

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
