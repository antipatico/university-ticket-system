from django.core.mail import send_mail
from django.urls import reverse
from django.utils.html import escape
from django.conf import settings

from uts_common.models import *


def delete_unused_ticket_event_attachments(max_age=43200):
    unused_attachments = TicketEventAttachment.objects.filter(event=None,
                                                              ts_delete__lt=timezone.now())
    deleted, _ = unused_attachments.delete()
    return f"deleted {deleted} unused uploaded files"


def add_ticket_event(ticket_id, owner_id, event_status, info=None, duplicate_id=None, new_owner_email=None,
                     attachments=[]):
    try:
        event_status = TicketStatus(event_status)
    except ValueError:
        raise ValueError("status is not valid")
    return TicketEvent.add_event(ticket_id, owner_id, event_status,
                                 info=info,
                                 duplicate_id=duplicate_id,
                                 new_owner_email=new_owner_email,
                                 attachments=attachments)


def new_ticket(user_id, owner_id, name, tags=[]):
    return Ticket.create(user_id, owner_id, name, tags)


def send_email_notification(event_id):
    event = TicketEvent.objects.get(pk=event_id)
    owner = event.owner
    ticket = event.ticket
    subscribers = ticket.subscribers.filter(profile__email_notifications=True)
    url = settings.UTS["BASE_URL"]
    ticket_url=f"{url}{reverse('uts_common:ticket_details', args=(ticket.id,))}"
    subject = f"[QATicket] Nuovo evento per {ticket.name} #{ticket.id}"
    message = f"{owner} ha {TicketActions[event.status]} ticket.\n" \
              f"Visita {ticket_url} per avere più informazioni."
    html_message = "<!DOCTYPE html5>" \
                   "<html>" \
                   f"<body><h1><a href='{url}'>QATicket</a></h1>" \
                   f"<p><strong>{owner}</strong> ha {TicketActions[event.status]} ticket #{ticket.id}: <a href='{ticket_url}'>{escape(ticket.name)}</a></p>" \
                   f"<p><pre>{escape(event.info) if event.status not in [TicketStatus.DUPLICATE, TicketStatus.ESCALATION] else ''}</pre></p>" \
                   "<footer><small>Email inviata automaticamente, per non ricevere più email smetti di seguire il ticket o cambia le impostazioni.</small></footer>" \
                   f"</body>" \
                   "</html>"
    for subscriber in subscribers:
        send_mail(subject, message, from_email=settings.EMAIL_FROM, recipient_list=[subscriber.email], html_message=html_message)
