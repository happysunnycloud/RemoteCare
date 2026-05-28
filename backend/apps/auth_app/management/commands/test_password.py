from django.core.management.base import BaseCommand

from apps.auth_app.services.assigner_service import get_assigner_by_login
from common.password import verify_password

class Command(BaseCommand):
    help = 'Test password verification'

    def handle(self, *args, **kwargs):
        row = get_assigner_by_login(
            'i.ivan'
        )

        if row is None:

            print('User not found')

            return

        is_valid = verify_password(
            '123',
            row[4]
        )

        print(is_valid)