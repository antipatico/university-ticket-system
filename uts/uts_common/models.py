from django.db import models
from django.contrib.auth.models import User


class TicketStatus(models.TextChoices):
    OPEN = 'OPEN', 'Aperto'
    CLOSED = 'CLOSED', 'Chiuso'
    DUPLICATE = 'DUPLICATE', 'Duplicato'
    ESCALATION = 'ESCALATION', 'Escalation'
    NOTE = 'NOTE', 'Note'
    INFO_NEEDED = 'INFO_NEEDED', 'Richiesta di Informazioni'
    ANSWER = 'ANSWER', 'Risposta'


class Owner(models.Model):
    class Meta:
        abstract = True


class Individual(Owner):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Organization(Owner):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    name = models.TextField(unique=True)


class Tag(models.Model):
    tag = models.TextField(unique=True)

    def __str__(self):
        return self.tag


class Ticket(models.Model):
    status = models.CharField(max_length=32, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag)
    ts_open = models.DateTimeField(auto_now_add=True)
    ts_last_modified = models.DateTimeField(auto_now=True)
    ts_closed = models.DateTimeField(null=True, blank=True)


class Event(models.Model):
    status = models.CharField(max_length=32, choices=TicketStatus.choices, default=TicketStatus.ANSWER)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(max_length=10*1024*1024, null=True, blank=True)
    answer = models.TextField()
