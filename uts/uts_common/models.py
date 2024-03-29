from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone
from polymorphic.models import PolymorphicModel


class TicketStatus(models.TextChoices):
    OPEN = 'OPEN', 'Aperto'
    CLOSED = 'CLOSED', 'Chiuso'
    DUPLICATE = 'DUPLICATE', 'Duplicato'
    ESCALATION = 'ESCALATION', 'Escalation'
    NOTE = 'NOTE', 'Note'
    INFO_NEEDED = 'INFO_NEEDED', 'Richiesta di Informazioni'
    ANSWER = 'ANSWER', 'Risposta'


class Owner(PolymorphicModel):
    pass


class Individual(Owner):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Organization(Owner):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administered_organizations")
    members = models.ManyToManyField(User, related_name="organizations", blank=True)
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.tag


class Ticket(models.Model):
    status = models.CharField(max_length=32, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    name = models.TextField(null=False, blank=False, max_length=255)
    subscribers = models.ManyToManyField(User, blank=True, related_name="subscribed_tickets")
    tags = models.ManyToManyField(Tag, blank=True)
    ts_open = models.DateTimeField(auto_now_add=True)
    ts_last_modified = models.DateTimeField(auto_now_add=True)
    ts_closed = models.DateTimeField(null=True, blank=True)

    @property
    def is_closed(self):
        return self.status == TicketStatus.CLOSED

    def is_owned_by(self, owner):
        if type(owner) is Individual:
            user = owner.user
            # Case 1: The ticket is owned by an individual, you need to check if the owner matches
            if type(self.owner) is Individual:
                return user.id == self.owner.user.id
            # Case 2: The ticket is owned by an Organization, you need to check if the owner is a member
            is_member = user in self.owner.members.all()
            is_admin = user.id == self.owner.admin.id
            return is_admin or is_member
        elif type(self.owner) is Organization:
            return self.owner.id == owner.id

    @classmethod
    @transaction.atomic
    def create(cls, user_id, owner_id, name, tags=[]):
        user = User.objects.get(pk=user_id)
        owner = Owner.objects.get(pk=owner_id)
        if type(owner) is Individual and owner.id != user.individual.id:
            raise ValueError("Non puoi creare un ticket come qualcun altro")
        if type(owner) is Organization and owner.admin.id != user.id and user not in owner.members.all():
            raise ValueError("Non puoi creare un ticket per un organizzazione di cui non fai parte")
        tags = [Tag.objects.get_or_create(tag=tag)[0] for tag in tags]
        ticket = Ticket.objects.create(owner=owner, name=name)
        ticket.tags.set(tags)
        event = TicketEvent.objects.create(ticket=ticket, owner=user.individual, status=TicketStatus.OPEN)
        if type(owner) is Organization:
            ticket.subscribers.set(owner.members.all())
            ticket.subscribers.add(owner.admin)
        ticket.subscribers.add(user)
        ticket.save()
        event.save()
        return ticket.id

    def __str__(self):
        return f"{self.name}"


class TicketEvent(models.Model):
    owner = models.ForeignKey(Owner,
                              on_delete=models.PROTECT)  # Note: this will refer to the old owner in case of Escalation
    status = models.CharField(max_length=32, choices=TicketStatus.choices, default=TicketStatus.ANSWER)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="events")
    timestamp = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, max_length=262144)

    @classmethod
    @transaction.atomic
    def add_event(cls, ticket_id, owner_id, event_status, info="", duplicate_id=None, new_owner_email=None, attachments=[]):
        ticket = Ticket.objects.get(pk=ticket_id)
        owner = Owner.objects.get(pk=owner_id)
        if type(event_status) != TicketStatus:
            raise ValueError("event status must be a TicketStatus")
        if event_status == TicketStatus.OPEN:
            if not ticket.is_owned_by(owner):
                raise ValueError("can't open a ticket you don't own")
            if not ticket.is_closed:
                raise ValueError("can't open a ticket that is already open")
        if event_status == TicketStatus.CLOSED:
            if not ticket.is_owned_by(owner):
                raise ValueError("can't close a ticket you don't own")
            if ticket.is_closed:
                raise ValueError("can't close a ticket that is already closed")
        if event_status == TicketStatus.ANSWER and ticket.is_closed:
            raise ValueError("can't reply to a closed ticket")
        if event_status == TicketStatus.NOTE and ticket.is_closed:
            raise ValueError("can't annotate a closed ticket")
        if event_status == TicketStatus.INFO_NEEDED and ticket.is_closed:
            raise ValueError("can't request more information on a closed ticket")
        if event_status == TicketStatus.DUPLICATE:
            if ticket.is_closed:
                raise ValueError("can't mark a ticket as duplicate if closed")
            duplicate_ticket = Ticket.objects.get(pk=duplicate_id)
            info = duplicate_id
        if event_status == TicketStatus.ESCALATION:
            if not ticket.is_owned_by(owner):
                raise ValueError("can't escalate a ticket you don't own")
            new_owner = User.objects.get(email=new_owner_email).individual
            ticket.owner = new_owner
            ticket.save()
        ticket_event = TicketEvent.objects.create(ticket=ticket, owner=owner, status=event_status, info=info)
        if event_status in [TicketStatus.OPEN, TicketStatus.CLOSED]:
            ticket.ts_closed = None if event_status is TicketStatus.OPEN else timezone.now()
            ticket.status = event_status
            ticket.save()
        if event_status in [TicketStatus.NOTE, TicketStatus.ANSWER, TicketStatus.INFO_NEEDED]:
            for attachment_id in attachments:
                attachment = TicketEventAttachment.objects.get(pk=attachment_id)
                if attachment.event is not None:
                    raise ValueError("can't attach a file to multiple tickets")
                if attachment.owner.id != owner.id:
                    return ValueError("can't attach a file you don't own")
                attachment.event = ticket_event
                attachment.ts_delete = None
                attachment.save()
        return ticket_event.id

    class Meta:
        ordering = ["timestamp"]


class TicketEventAttachment(models.Model):
    event = models.ForeignKey(TicketEvent, on_delete=models.CASCADE, related_name="attachments", null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    name = models.TextField(max_length=255)
    file = models.FileField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ts_delete = models.DateTimeField(default=timezone.now() + timedelta(hours=12), null=True)


class Notification(models.Model):
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
    event = models.ForeignKey(TicketEvent, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=False)


User.full_name = property(lambda u: f"{u.username}" if not u.first_name else (f"{u.first_name}" if not u.last_name else f"{u.first_name} {u.last_name}"))
User.all_organizations = property(lambda u: u.organizations.all().union(u.administered_organizations.all()))


TicketActions = {
    TicketStatus.OPEN: "aperto il",
    TicketStatus.CLOSED: "chiuso il",
    TicketStatus.DUPLICATE: "marcato come duplicato il",
    TicketStatus.ESCALATION: "trasferito la proprietà del",
    TicketStatus.NOTE: "aggiunto una nota al",
    TicketStatus.INFO_NEEDED: "richiesto maggiori informazioni per il",
    TicketStatus.ANSWER: "risposto al"
}
