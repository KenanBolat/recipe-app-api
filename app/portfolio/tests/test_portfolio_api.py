"""
Tests for portfolio APIs.
"""
from decimal import Decimal

import tempfile
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Portfolio,
                         Tag,
                         Ingredient)

from portfolio.serializers import (
    PortfolioSerializer,
    PortfolioDetailSerializer,
)

PORTFOLIOS_URL = reverse('portfolio:portfolio-list')


def detail_url(portfolio_id):
    """Create and return a portfolio url."""
    return reverse('portfolio:portfolio-detail', args=[portfolio_id])


def create_portfolio(user, **params):
    """Create and retrun a sample portfolio. Helper function"""
    defaults = {
        'title': 'Sample Portfolio Title',
        'description': 'Sample description',
        'link': 'http://example.com/portfolio.pdf',
    }
    defaults.update(params)

    portfolio = Portfolio.objects.create(user=user, **defaults)
    return portfolio


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicPortfolioAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PORTFOLIOS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateportfolioAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_portfolios(self):
        """Test retrieving a list of portfolios."""
        pass

    def test_portfolio_list_limited_to_user(self):
        """Test list of portfolios is limited to authenticated user."""
        pass

    def test_get_portfolio_detail(self):
        """Test get portfolio detail."""
        pass
