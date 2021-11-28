from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):
    """ Command Create/Delete amenities """

    help = 'This Command create or delete amenities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create',
            action='store_true',
            help='Create amenities'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete amenities'
        )


    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        if options['create']:
            for i in amenities:
                if not Amenity.objects.filter(name=i):
                    Amenity.objects.create(name=i)
            self.stdout.write(self.style.SUCCESS(f'{len(amenities)} amenities created!'))

        elif options['delete']:
            Amenity.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All amenities deleted!'))

        else:
            self.stdout.write(self.style.ERROR('Options are not given. (--create or --delete)'))
    