from django.core.management.base import BaseCommand, CommandError
from uts_common.models import *
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Populate the database for development purposes'

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            admin = User.objects.create_user('admin', 'admin@localhost', 'admin', is_staff=True, is_superuser=True)
            admin.first_name = "Administrator"
            admin.save()

            user1 = User.objects.create_user('user1', 'carlo.bianchi@localhost', 'user1', first_name="Carlo", last_name="Bianchi")
            user2 = User.objects.create_user('user2', 'mario.rossi@localhost', 'user2', first_name="Mario", last_name="Rossi")
            user3 = User.objects.create_user('user3', 'luigi.verdi@localhost', 'user3', first_name="Luigi", last_name="Verdi")
            user4 = User.objects.create_user('user4', 'john.doe@localhost', 'user4', first_name="John", last_name="Doe")

            org1 = Organization.objects.create(name="Docenti", admin=admin)
            org1.members.add(user1)
            org1.members.add(user4)
            org2 = Organization.objects.create(name="Alunni", admin=user2)
            org2.members.add(user3)

            ticket_id = Ticket.create(admin.id, admin.individual.id, f"Ticket di esempio!", tags=["prova", "esempio"])
            ticket = Ticket.objects.get(pk=ticket_id)
            ticket.subscribers.add(user2)
            ticket.subscribers.add(user3)
            TicketEvent.add_event(ticket_id, admin.individual.id, TicketStatus.NOTE, "Descrizione del problema qui")
            TicketEvent.add_event(ticket_id, user2.individual.id, TicketStatus.INFO_NEEDED)
            TicketEvent.add_event(ticket_id, user3.individual.id, TicketStatus.ANSWER, "Il problema è stato risolto nella runione del 20 Aprile")
            TicketEvent.add_event(ticket_id, admin.individual.id, TicketStatus.CLOSED)

        except IntegrityError as e:
            print(e)
            print("ERROR: db seems to already contain some data.")
