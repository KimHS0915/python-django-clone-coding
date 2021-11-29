from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    """ Command Create users """

    help = 'This Command create or delete users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete users'
        )
        parser.add_argument(
            '--number',
            type=int,
            help='How many users you want to create'
        )

    def handle(self, *args, **options):
        if options['number']:
            number = options.get('number')
            seeder = Seed.seeder()
            seeder.add_entity(User, number, {'is_staff': False, 'is_superuser': False})
            seeder.execute()
            self.stdout.write(self.style.SUCCESS(f'{number} users created!'))
        
        elif options['delete']:
            users = User.objects.filter(is_superuser=False)
            number = len(users)
            users.delete()
            self.stdout.write(self.style.SUCCESS(f'{number} users deleted!'))

        else:
            self.stdout.write(self.style.ERROR('Options are not given. (--number NUMBER or --delete)'))
