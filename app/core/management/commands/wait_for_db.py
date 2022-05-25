"""
Django command to wait for the database to be available
"""
from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycop2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """ stub for handle command """
        pass
