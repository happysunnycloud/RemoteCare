from django.core.management.base import BaseCommand
from common.db import get_connection

class Command(BaseCommand):
    help = 'Test PostgreSQL connection'
    def handle(self, *args, **kwargs):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        print(result)
        cursor.close()
        connection.close()