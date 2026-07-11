import random

from django.core.management.base import BaseCommand
from django.db.models import Model
from faker import Faker

from ToDoApp.models import Task
from blog.models import Category, Posts
from account.models import UserProfile, User


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker(['en_US','fa_IR'])

    def handle(self, *args, **options):


        for u in range(1,5):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            birth_date = self.fake.date_of_birth()
            email = self.fake.email()
            password = "Mn00137400"
            is_verified = self.fake.boolean(chance_of_getting_true=50)
            is_active = self.fake.boolean(chance_of_getting_true=50)

            user = User.objects.create_user(email=email,
                                            password=password,
                                            is_verified=is_verified,
                                            is_active=is_active)

            profile = UserProfile.objects.create(user=user,
                                                 first_name=first_name,
                                                 last_name=last_name,
                                                 birth_date=birth_date)

            for t in range(1,5):
                title = self.fake.sentence(nb_words=3)
                description = self.fake.paragraph(nb_sentences=3)
                status = random.choice([True, False])

                task = Task.objects.create(user=profile,
                                            title=title,
                                            description=description,
                                            status=status)
