from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from uts_common.models import Ticket
from uts_report.generators import *


class DocxHttpResponse(HttpResponse):
    def __init__(self, *args, document_name=None, **kwargs):
        kwargs["content_type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        super().__init__(*args, **kwargs)
        document_name = "document" if document_name is None else document_name
        self["Content-Disposition"] = f"attachment; filename={document_name}.docx"


def report_generator(request):
    pass


@login_required
def generate_ticket_report(request, pk):
    ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
    document_stream = document_from_ticket(ticket, request.build_absolute_uri(settings.MEDIA_URL))
    return DocxHttpResponse(document_stream, document_name=f"ticket-{ticket.id}-report")


@login_required
def generate_closed_tickets_report(request):
    tickets = Ticket.objects.filter(~Q(ts_closed=None))
    document_stream = document_from_many_tickets(tickets, "Ticket chiusi", request.build_absolute_uri(settings.MEDIA_URL))
    return DocxHttpResponse(document_stream, document_name=f"ticket-chiusi-report")


@login_required
def generate_opened_lastyear_tickets_report(request):
    tickets = Ticket.objects.filter(ts_open__gte=timezone.datetime(year=timezone.now().year, month=1, day=1))
    document_stream = document_from_many_tickets(tickets, "Ticket aperti quest'anno", request.build_absolute_uri(settings.MEDIA_URL))
    return DocxHttpResponse(document_stream, document_name=f"ticket-aperti-anno-corrente-report")


@login_required
def generate_opened_lastyear_stillopen_tickets_report(request):
    tickets = Ticket.objects.filter(
        Q(ts_open__gte=timezone.datetime(year=timezone.now().year, month=1, day=1)) &
        Q(ts_closed=None))
    document_stream = document_from_many_tickets(tickets, "Ticket aperti quest'anno ancora aperti", request.build_absolute_uri(settings.MEDIA_URL))
    return DocxHttpResponse(document_stream, document_name=f"ticket-aperti-anno-corrente-ancora-aperti-report")
