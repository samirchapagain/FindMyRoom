from django.core.management.base import BaseCommand
from started.models import Room

class Command(BaseCommand):
    help = 'Populate database with sample rooms'

    def handle(self, *args, **options):
        rooms_data = [
            {
                'title': 'Premium Studio Apartment',
                'room_type': 'studio',
                'location': 'Downtown',
                'price': 18500,
                'description': 'Modern studio in downtown area with stunning city views',
                'contact_phone': '+91 98765 43210',
                'contact_email': 'owner1@email.com',
                'area_m2': 45,
                'beds': 1,
                'baths': 1,
            },
            {
                'title': 'Cozy Private Room',
                'room_type': 'private',
                'location': 'Near University',
                'price': 9800,
                'description': 'Quiet room in a friendly shared house near university',
                'contact_phone': '+91 98765 43211',
                'contact_email': 'owner2@email.com',
                'area_m2': 25,
                'beds': 1,
                'baths': 1,
            },
            {
                'title': 'Modern City Apartment',
                'room_type': 'apartment',
                'location': 'Business District',
                'price': 32000,
                'description': 'Spacious 2-bedroom apartment in the heart of the city',
                'contact_phone': '+91 98765 43212',
                'contact_email': 'owner3@email.com',
                'area_m2': 85,
                'beds': 2,
                'baths': 2,
            },
            {
                'title': 'Luxury Penthouse',
                'room_type': 'apartment',
                'location': 'Downtown',
                'price': 55000,
                'description': 'Exclusive penthouse with panoramic city views and premium amenities',
                'contact_phone': '+91 98765 43213',
                'contact_email': 'owner4@email.com',
                'area_m2': 120,
                'beds': 3,
                'baths': 3,
            },
            {
                'title': 'Student Shared Room',
                'room_type': 'shared',
                'location': 'Near University',
                'price': 6500,
                'description': 'Affordable shared accommodation perfect for students',
                'contact_phone': '+91 98765 43214',
                'contact_email': 'owner5@email.com',
                'area_m2': 20,
                'beds': 1,
                'baths': 1,
            },
            {
                'title': 'Executive Suite',
                'room_type': 'studio',
                'location': 'Business District',
                'price': 28000,
                'description': 'Fully furnished executive suite with modern amenities',
                'contact_phone': '+91 98765 43215',
                'contact_email': 'owner6@email.com',
                'area_m2': 60,
                'beds': 1,
                'baths': 1,
            }
        ]

        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                title=room_data['title'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f'Created room: {room.title}')
            else:
                self.stdout.write(f'Room already exists: {room.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated rooms!'))