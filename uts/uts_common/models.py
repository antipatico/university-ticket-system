from django.db import models
from django.contrib.auth.models import User
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
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.TextField(unique=True)

    def __str__(self):
        return self.tag


class Ticket(models.Model):
    status = models.CharField(max_length=32, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return f"{self.name}"


class TicketEvent(models.Model):
    owner = models.ForeignKey(Owner,
                              on_delete=models.PROTECT)  # Note: this will refer to the old owner in case of Escalation
    status = models.CharField(max_length=32, choices=TicketStatus.choices, default=TicketStatus.ANSWER)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="events")
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(max_length=10 * 1024 * 1024, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["timestamp"]


class Notification(models.Model):
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
    event = models.ForeignKey(TicketEvent, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)


User.full_name = property(lambda u: f"{u.username}" if not u.first_name else (f"{u.first_name}" if not u.last_name else f"{u.first_name} {u.last_name}"))
