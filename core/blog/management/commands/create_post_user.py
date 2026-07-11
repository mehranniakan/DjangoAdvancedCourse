import random

from django.core.management.base import BaseCommand
from faker import Faker

from account.models import UserProfile, User
from blog.models import Category, Posts


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker(['en_US', 'fa_IR'])
        self.cat_list = ['Fun',
                         'Tech',
                         'Science',
                         'Politics',
                         'Engineering',
                         'City']

    def handle(self, *args, **options):

        for c in self.cat_list:
            Category.objects.get_or_create(name=c)

        for u in range(1, 20):
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

            for p in range(1, 20):
                title = self.fake.sentence(nb_words=3)
                content = self.fake.paragraph(nb_sentences=3)
                category = Category.objects.get(name=random.choice(self.cat_list))
                slug = f'{title}-{category.name}'
                status = random.choice([True, False])

                Posts.objects.create(author=profile,
                                     title=title,
                                     content=content,
                                     category=category,
                                     slug=slug,
                                     status=status)
