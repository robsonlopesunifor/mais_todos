from contextlib import suppress

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from decouple import config


class Command(BaseCommand):
    help = "Seed database with sample data"

    def add_arguments(self, parser):
        parser.add_argument("--create-superuser", action="store_true", dest="create_superuser")

    def handle(self, *args, **kwargs):
        self.create_superuser = kwargs["create_superuser"]
        with suppress(Exception):
            if self.create_superuser:
                create_superuser()


def create_superuser():
    username = config("TEST_APP_USERNAME", default="pedro", cast=str)
    password = config("TEST_APP_PASSWORD", default="123456", cast=str)
    get_user_model().objects.create_superuser(username, None, password)
