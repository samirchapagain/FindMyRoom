from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from started.models import Owner, Client, UserProfile

class Command(BaseCommand):
    help = 'Create test users for Owner and Client roles'

    def handle(self, *args, **options):
        # Create test owner
        if not User.objects.filter(username='testowner').exists():
            owner_user = User.objects.create_user(
                username='testowner',
                email='owner@test.com',
                password='testpass123'
            )
            UserProfile.objects.create(user=owner_user)
            Owner.objects.create(
                user=owner_user,
                phone='+1234567890',
                address='123 Main St, City, State'
            )
            self.stdout.write(self.style.SUCCESS('Created test owner: testowner/testpass123'))

        # Create test client
        if not User.objects.filter(username='testclient').exists():
            client_user = User.objects.create_user(
                username='testclient',
                email='client@test.com',
                password='testpass123'
            )
            UserProfile.objects.create(user=client_user)
            Client.objects.create(
                user=client_user,
                phone='+0987654321',
                preferred_location='Downtown Area'
            )
            self.stdout.write(self.style.SUCCESS('Created test client: testclient/testpass123'))

        self.stdout.write(self.style.SUCCESS('Test users created successfully!'))