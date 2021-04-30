from django.core.management.base import BaseCommand, CommandError
from uts_common.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Create a default admin account'

    def add_arguments(self, parser):
#        parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        try:
            user = User.objects.create_user('admin', 'admin@localhost', 'admin', is_staff=True, is_superuser=True)
            user.save()
        except IntegrityError:
            print("ERROR: admin account already existing.")
