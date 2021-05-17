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
