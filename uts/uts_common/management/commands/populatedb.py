from django.core.management.base import BaseCommand, CommandError
from uts_common.models import *
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Populate the database for development purposes'

    def handle(self, *args, **options):
        try:
            admin = User.objects.create_user('admin', 'admin@localhost', 'admin', is_staff=True, is_superuser=True)
            admin.first_name = "admin"
            admin.last_name = "admin"
            admin.save()

            for i in range(5):
                ticket = Ticket.objects.create(owner=admin.individual,
                                               name=f"Ticket #{i}",
                                               description=f"Short ticket #{i} description")
                event1 = TicketEvent.objects.create(owner=admin.individual,
                                                    status=TicketStatus.ANSWER,
                                                    ticket=ticket,
                                                    info="Answer body here. Lorem ipsum dolor sit amet")
                event2 = TicketEvent.objects.create(owner=admin.individual,
                                                    status=TicketStatus.DUPLICATE,
                                                    ticket=ticket,
                                                    info="3")
                event3 = TicketEvent.objects.create(owner=admin.individual,
                                                    status=TicketStatus.INFO_NEEDED,
                                                    ticket=ticket,
                                                    info="")
                ticket.save()
                event1.save()
                event2.save()
                event3.save()

        except IntegrityError:
            print("ERROR: db seems to already contain some data.")
