from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    """ Command Create/Delete facilities """

    help = 'This Command create or delete facilities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create',
            action='store_true',
            help='Create facilities'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete facilities'
        )


    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        if options['create']:
            for i in facilities:
                if not Facility.objects.filter(name=i):
                    Facility.objects.create(name=i)
            self.stdout.write(self.style.SUCCESS(f'{len(facilities)} facilities created!'))

        elif options['delete']:
            Facility.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All facilities deleted!'))

        else:
            self.stdout.write(self.style.ERROR('Options are not given. (--create or --delete)'))
    