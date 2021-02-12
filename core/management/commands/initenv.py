from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Initialize the project environment, i.e. do things like: run "
        "migrations, create superuser accounts, populate the database with "
        "some initial data). If the environment is already set up, it will "
        "be reset to a starting point."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'env_type',
            choices=['dev', 'prod'],
            help="Which type of environment to set up?",
        )

    def handle(self, *args, **options):
        handler = getattr(self, f"init_{options['env_type']}")
        handler()

    def init_dev(self):
        """
        Initialize DEVELOPER environment.
        """
        self.stdout.write("Flushing the database...")
        call_command('flush', '--no-input')
        self.stdout.write(self.style.SUCCESS("DONE\n"))

        self.stdout.write("Running database migrations...")
        call_command('migrate')
        self.stdout.write("")

        self.stdout.write("Creating a superuser account...")
        User = get_user_model()
        User.objects.create_superuser(
            username='admin',
            password='dummypass',
            email='admin@dummy.com',
        )
        self.stdout.write(self.style.SUCCESS("DONE\n"))

        self.stdout.write("Populating the database:")
        call_command('filldevdb')

    def init_prod(self):
        """
        Initialize PRODUCTION environment.
        """
        raise NotImplementedError