from django.core.management.base import BaseCommand
from apps.auth_app.services.assigner_service import get_assigners

class Command(BaseCommand):
    help = 'Test assigner service'

    def handle(self, *args, **kwargs):
        rows = get_assigners()

        print(rows)