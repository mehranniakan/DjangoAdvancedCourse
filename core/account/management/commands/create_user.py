from account.models import User, UserProfile
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker(["en_US", "fa_IR"])

    def handle(self, *args, **options):

        for i in range(50):
            user = User.objects.create(
                email=self.fake.email(),
                is_verified=True,
            )
            user.set_password("Mn00137400")
            user.save()

            UserProfile.objects.create(
                user=user,
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
            )
