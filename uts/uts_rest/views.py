from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from uts_rest.serializers import *


class AuthenticatedViewSet(ViewSet):
    permission_classes = [IsAuthenticated]


# Get the 3 most recent tickets the user "interacted with"
class RecentActivitiesView(AuthenticatedViewSet):
    def list(self, request):
        tickets = Ticket.objects.filter(
            Q(owner_id=request.user.individual.id) | Q(subscribers=request.user)).distinct().order_by(
            "-ts_last_modified")[:3]
        serializer = TicketSerializer(tickets, max_events=3, list_events=True, many=True)
        return Response(serializer.data)


class SubscribedTicketsView(AuthenticatedViewSet):
    def list(self, request):
        tickets = Ticket.objects.filter(Q(subscribers=request.user) & ~Q(owner_id=request.user.individual.id)).order_by(
            "ts_closed", "-ts_open")
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketsView(AuthenticatedViewSet):
    def list(self, request):
        tickets = Ticket.objects.filter(owner_id=request.user.individual.id).order_by("ts_closed", "-ts_open")
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk)
        serializer = TicketSerializer(ticket, user=request.user, list_events=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk)
        subscription = request.data.get("is_subscribed", None)
        if subscription is not None and type(subscription) is bool:
            if subscription:
                ticket.subscribers.add(request.user)
            else:
                ticket.subscribers.remove(request.user)
            ticket.save()
            serializer = TicketSerializer(ticket, user=request.user, list_events=True)
            return Response(serializer.data)
        return Response({"detail": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class TicketEventsView(AuthenticatedViewSet):
    @transaction.atomic
    def create(self, request):
        owner = request.user.individual
        info = request.data.get("info", "")
        info = info if info is not None else ""
        ticket_id = request.data.get("ticket_id", None)
        duplicate_id = request.data.get("duplicate_id", None)
        new_owner_email = request.data.get("new_owner_email", None)
        attachments = request.data.get("attachments", [])
        try:
            event_status = TicketStatus(request.data.get("status", None))
        except ValueError:
            return Response({"detail": "status is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=ticket_id)

        if event_status == TicketStatus.OPEN:
            if not ticket.is_owned_by(owner):
                return Response({"detail": "can't open a ticket you don't own"}, status=status.HTTP_401_UNAUTHORIZED)
            if not ticket.is_closed:
                return Response({"detail": "can't open a ticket that is already open"}, status=status.HTTP_403_FORBIDDEN)

        if event_status == TicketStatus.CLOSED:
            if not ticket.is_owned_by(owner):
                return Response({"detail": "can't close a ticket you don't own"}, status=status.HTTP_401_UNAUTHORIZED)
            if ticket.is_closed:
                return Response({"detail": "can't close a ticket that is already closed"}, status=status.HTTP_403_FORBIDDEN)

        if event_status == TicketStatus.ANSWER:
            if ticket.is_closed:
                return Response({"detail": "can't reply to a closed ticket"}, status=status.HTTP_400_BAD_REQUEST)
            if type(info) is not str or len(info) < 1:
                return Response({"detail": "can't reply with an empty answer"}, status=status.HTTP_400_BAD_REQUEST)

        if event_status == TicketStatus.NOTE:
            if ticket.is_closed:
                return Response({"detail": "can't annotate a closed ticket"}, status=status.HTTP_400_BAD_REQUEST)
            if type(info) is not str or len(info) < 1:
                return Response({"detail": "can't add an empty note"}, status=status.HTTP_400_BAD_REQUEST)

        if event_status == TicketStatus.INFO_NEEDED:
            if ticket.is_closed:
                return Response({"detail": "can't request more information on a closed ticket"}, status=status.HTTP_400_BAD_REQUEST)

        if event_status == TicketStatus.DUPLICATE:
            if ticket.is_closed:
                return Response({"detail": "can't mark a ticket as duplicate if closed"}, status=status.HTTP_400_BAD_REQUEST)
            if ticket.id == duplicate_id:
                return Response({"detail": "you can't mark a ticket as a duplicate of itself"}, status=status.HTTP_400_BAD_REQUEST)
            duplicate_ticket = get_object_or_404(Ticket, pk=duplicate_id)
            info = duplicate_id

        if event_status == TicketStatus.ESCALATION:
            if not ticket.is_owned_by(owner):
                return Response({"detail": "can't escalate a ticket you don't own"}, status=status.HTTP_401_UNAUTHORIZED)
            new_user = get_object_or_404(User.objects.all(), email=new_owner_email)
            new_owner = new_user.individual
            if new_owner.id == owner.id:
                return Response({"detail": "can't escalate a ticket to yourself"}, status=status.HTTP_400_BAD_REQUEST)
            ticket.owner = new_owner
            ticket.save()

        ticket_event = TicketEvent.objects.create(ticket=ticket, owner=owner, status=event_status, info=info)
        if event_status in [TicketStatus.OPEN, TicketStatus.CLOSED]:
            ticket.ts_closed = None if event_status is TicketStatus.OPEN else timezone.now()
            ticket.status = event_status
            ticket.save()

        if event_status in [TicketStatus.NOTE, TicketStatus.ANSWER, TicketStatus.INFO_NEEDED]:
            for attachment_id in attachments:
                attachment = get_object_or_404(TicketEventAttachment.objects.all(), pk=attachment_id)
                if attachment.event is not None:
                    return Response({"detail": "can't attach a file to multiple tickets"}, status=status.HTTP_400_BAD_REQUEST)
                if attachment.owner.id != owner.id:
                    return Response({"detail": "can't attach a file you don't own"}, status=status.HTTP_403_FORBIDDEN)
                attachment.event = ticket_event
                attachment.save()

        serializer = TicketSerializer(ticket, list_events=True, user=request.user)
        return Response(serializer.data)


class AttachmentsView(AuthenticatedViewSet):
    parser_class = (FileUploadParser,)

    def create(self, request):
        if 'file' not in request.data:
            return Response({"detail": "empty file"}, status=status.HTTP_400_BAD_REQUEST)
        f = request.data.get("file", None)
        attachment = TicketEventAttachment.objects.create(owner=request.user.individual, name=f.name, file=f)
        attachment.save()
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        attachment = get_object_or_404(TicketEventAttachment.objects.all(), pk=pk)
        if request.user.individual.id != attachment.owner.id:
            return Response({"detail": "can't delete a file you don't own"}, status=status.HTTP_403_FORBIDDEN)
        attachment.delete()
        return Response({}, status=status.HTTP_200_OK)


class OrganizationsView(AuthenticatedViewSet):
    def list(self, request):
        organizations = request.user.organizations.all()
        administered_org = request.user.administered_organizations.all()
        serializer = OrganizationSerializer(administered_org.union(organizations), user=request.user, many=True)
        return Response(serializer.data)
