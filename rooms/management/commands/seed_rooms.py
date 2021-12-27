import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms.models import Amenity, Facility, HouseRule, Photo, Room, RoomType
from users.models import User


class Command(BaseCommand):
    """ Command Create rooms """

    help = 'This Command create rooms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            default=1,
            type=int,
            help='How many rooms you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        all_users = User.objects.all()
        room_type = RoomType.objects.all()
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()
        seeder.add_entity(
            Room, number, {
                'name': lambda x: seeder.faker.address(),
                'host': lambda x: random.choice(all_users),
                'room_type': lambda x: random.choice(room_type),
                'guests': lambda x: random.randint(1, 19),
                'price': lambda x: random.randint(1, 300),
                'beds': lambda x: random.randint(1, 5),
                'bedrooms': lambda x: random.randint(1, 5),
                'baths': lambda x: random.randint(1, 5),
            }
        )
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        for pk in created_clean:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(5, 10)):
                Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f'/room_photos/{random.randint(1, 31)}.webp',
                )
            for amenity in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)
            for facility in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)
            for rule in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(rule)
        self.stdout.write(self.style.SUCCESS(f'{number} rooms created!'))
