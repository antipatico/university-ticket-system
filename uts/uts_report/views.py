from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from uts_common.models import Ticket
from uts_report.generators import document_from_ticket


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
    document_stream = document_from_ticket(ticket, base_url=request.build_absolute_uri(settings.MEDIA_URL))

    response = DocxHttpResponse(document_stream, document_name=f"ticket-{ticket.id}-report")
    return response