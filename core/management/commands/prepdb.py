from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from core import const
from accounts.models import Group

SELLERS_GROUPNAME = const.SELLERS_GROUPNAME


def create_seller_group():
    sellers = Group.objects.create(name=SELLERS_GROUPNAME)
    sellers.permissions.add(
        # Permissions to manage the seller's windows
        Permission.objects.get(codename='add_window'),
        Permission.objects.get(codename='change_window'),
        Permission.objects.get(codename='delete_window'),
        Permission.objects.get(codename='view_window'),

        # Permissions to edit the seller's profile
        Permission.objects.get(codename='change_seller'),
        Permission.objects.get(codename='view_seller'),
        # phones
        Permission.objects.get(codename='add_phone'),
        Permission.objects.get(codename='change_phone'),
        Permission.objects.get(codename='delete_phone'),
        Permission.objects.get(codename='view_phone'),
        # places
        Permission.objects.get(codename='add_place'),
        Permission.objects.get(codename='change_place'),
        Permission.objects.get(codename='delete_place'),
        Permission.objects.get(codename='view_place'),
    )


class Command(BaseCommand):
    help = (
        "Fill the project database with data essential to both production and "
        "development environments."
    )

    def handle(self, *args, **options):
        self.stdout.write(f"Creating group '{SELLERS_GROUPNAME}'...")
        try:
            Group.objects.get(name=SELLERS_GROUPNAME)
            self.stdout.write(self.style.NOTICE(
                f"Group '{SELLERS_GROUPNAME}' already exists. Skipping."
            ))
        except Group.DoesNotExist:
            create_seller_group()
            self.stdout.write(self.style.SUCCESS("DONE"))