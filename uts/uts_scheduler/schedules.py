from datetime import timedelta
from django.utils import timezone
from uts_common.models import *


def delete_unused_ticket_event_attachments(max_age=43200):
    unused_attachments = TicketEventAttachment.objects.filter(event=None, timestamp__lt=timezone.now()-timedelta(hours=12))
    deleted, _ = unused_attachments.delete()
    return f"deleted {deleted} unused uploaded files"
