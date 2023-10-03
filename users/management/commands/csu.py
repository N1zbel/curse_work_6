import os
import json
from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from curse_project.settings import BASE_DIR
from users.models import User


class Command(BaseCommand):
    help = 'создание суперпользователя'

    def handle(self, *args, **options):
        Group.objects.all().delete()
        User.objects.all().delete()
        user = User.objects.create(
            email=os.getenv('GMAIL'),
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True
        )

        user.set_password('password')
        user.save()
        with open(BASE_DIR / 'users/fixtures/groups.json', 'r', encoding='UTF-8') as file:
            group_data = json.load(file)
            for item in group_data:
                group = Group.objects.create(
                    pk=item['pk'],
                    name=item['fields']['name'],
                )
                group.permissions.set(item['fields']['permissions'])
