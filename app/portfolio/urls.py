"""
URL mappings for the portfolio app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from portfolio import views

router = DefaultRouter()
router.register('portfolios', views.PortfolioViewSet)
router.register('tags', views.TagViewSet)

app_name = 'portfolio'

urlpatterns = [
    path('', include(router.urls)),
]
