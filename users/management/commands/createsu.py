import os
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=os.environ.get('ADMIN_ID'))
        if not admin:
            User.objects.create_superuser(
                os.environ.get('ADMIN_ID'),
                os.environ.get('ADMIN_EMAIL'),
                os.environ.get('ADMIN_PASSWORD'),
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser Created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser Exists'))
