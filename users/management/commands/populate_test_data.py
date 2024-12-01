import random
from django.core.management.base import BaseCommand
from users.models import CustomUser, UserContact, PhoneNumber

class Command(BaseCommand):
    help = 'Populate database with random sample data'

    def handle(self, *args, **options):
        # Delete all users except the admin
        user_to_keep = CustomUser.objects.get(phone_number='1234567890')
        users_to_delete = CustomUser.objects.exclude(id=user_to_keep.id)
        users_to_delete.delete()

        # Delete all other data
        UserContact.objects.all().delete()
        PhoneNumber.objects.all().delete()

        # Generate random sample data
        for _ in range(50):  # Adjust the number based on your needs
            user = CustomUser.objects.create(
                name=f'CustomUser{random.randint(1, 100)}',
                phone_number=f'{random.randint(1000000000, 9999999999)}',
                email=f'user{random.randint(1, 100)}@example.com'
            )

            # Create contacts for each user
            for _ in range(random.randint(1, 10)):
                contact = UserContact.objects.create(
                    user=user,
                    contact_name=f'Contact{random.randint(1, 100)}',  
                    phone_number=f'{random.randint(1000000000, 9999999999)}'
                )

            # Create random phone numbers
            for _ in range(random.randint(1, 10)):
                PhoneNumber.objects.create(
                    name=f'Phone{random.randint(1, 100)}',
                    number=f'{random.randint(1000000000, 9999999999)}',
                    spam_likelihood=random.randint(0, 100)
                )

        self.stdout.write(self.style.SUCCESS('Database populated with random sample data'))