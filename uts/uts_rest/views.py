from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import dateparse
from django_q.tasks import schedule
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        owner_id = request.user.individual.id
        info = request.data.get("info", "")
        info = info if info is not None else ""
        ticket_id = request.data.get("ticket_id", None)
        duplicate_id = request.data.get("duplicate_id", None)
        new_owner_email = request.data.get("new_owner_email", None)
        attachments = request.data.get("attachments", [])
        schedule_datetime = request.data.get("schedule_datetime", "")

        try:
            event_status = TicketStatus(request.data.get("status", None))
        except ValueError:
            return Response({"detail": "status is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        if event_status == TicketStatus.ANSWER and (type(info) is not str or len(info) < 1):
            return Response({"detail": "can't reply with an empty answer"}, status=status.HTTP_400_BAD_REQUEST)
        if event_status == TicketStatus.NOTE and (type(info) is not str or len(info) < 1):
            return Response({"detail": "can't add an empty note"}, status=status.HTTP_400_BAD_REQUEST)
        if event_status == TicketStatus.DUPLICATE and ticket_id == duplicate_id:
            return Response({"detail": "can't mark a ticket as a duplicate of itself"},
                            status=status.HTTP_400_BAD_REQUEST)
        if event_status == TicketStatus.ESCALATION:
            new_user = get_object_or_404(User.objects.all(), email=new_owner_email)
            new_owner = new_user.individual
            if new_owner.id == owner_id:
                return Response({"detail": "can't escalate a ticket to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_schedule = dateparse.parse_datetime(schedule_datetime)
            if schedule_datetime != "" and to_schedule is None:
                raise TypeError()
        except TypeError:
            return Response({"detail": "scheduled datetime is not a valid datetime"},
                            status=status.HTTP_400_BAD_REQUEST)

        if to_schedule is not None:
            if to_schedule < timezone.now() + timedelta(minutes=5):
                return Response({"detail": "schedule datetime is too near the present (or maybe even in the past)"},
                                status=status.HTTP_400_BAD_REQUEST)
            for attachment_id in attachments:
                attachment = TicketEventAttachment.objects.get(pk=attachment_id)
                if attachment.event is not None:
                    return Response({"detail": "can't attach a file to multiple tickets"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if attachment.owner.id != owner_id:
                    return Response({"detail": "can't attach a file you don't own"}, status=status.HTTP_400_BAD_REQUEST)
                attachment.ts_delete = to_schedule + timedelta(hours=1)
                attachment.save()

            schedule('uts_scheduler.schedules.add_ticket_event',
                     ticket_id, owner_id, str(event_status),
                     info=info, duplicate_id=duplicate_id, new_owner_email=new_owner_email, attachments=attachments,
                     next_run=to_schedule,
                     schedule_type='O')
        else:
            try:
                TicketEvent.add_event(ticket_id, owner_id, event_status, info, duplicate_id, new_owner_email,
                                      attachments)
            except ValueError as e:
                return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            except Ticket.DoesNotExist:
                return Response({"detail": "invalid ticket"}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({"detail": "invalid new owner email"}, status=status.HTTP_404_NOT_FOUND)
            except TicketEventAttachment.DoesNotExist:
                return Response({"detail": "invalid attachment"}, status=status.HTTP_404_NOT_FOUND)

        ticket = get_object_or_404(Ticket.objects.all(), pk=ticket_id)
        serializer = TicketSerializer(ticket, list_events=True, user=request.user)
        return Response(serializer.data)


class AttachmentsView(AuthenticatedViewSet):
    parser_class = (FileUploadParser,)

    def create(self, request):
        if 'file' not in request.data:
            return Response({"detail": "empty file"}, status=status.HTTP_400_BAD_REQUEST)
        f = request.data.get("file", None)
        if f.size > settings.UTS['MAX_ATTACHMENT_FILE_SIZE']:
            return Response({"detail": "file size exceeds limits (10MB)"}, status=status.HTTP_400_BAD_REQUEST)
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
        serializer = OrganizationSerializer(request.user.all_organizations, user=request.user, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def partial_update(self, request, pk=None):
        organization = get_object_or_404(Organization.objects.all(), pk=pk)
        if request.user.id != organization.admin.id:
            return Response({"detail": "operation not allowed, you need to the organization's admin"}, status=status.HTTP_403_FORBIDDEN)
        new_user_email = request.data.get("new_user_email", None)
        user = get_object_or_404(User.objects.all(), email=new_user_email)
        if user in organization.members.all() or user.id == organization.admin.id:
            return Response({}, status=status.HTTP_200_OK)
        organization.members.add(user)
        return Response({}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request, pk=None):
        organization = get_object_or_404(Organization.objects.all(), pk=pk)
        if request.user.id != organization.admin.id:
            return Response({"detail": "operation not allowed, you need to the organization's admin"}, status=status.HTTP_403_FORBIDDEN)
        delete_user_email = request.data.get("delete_user_email", None)
        user = get_object_or_404(User.objects.all(), email=delete_user_email)
        organization.members.remove(user)
        return Response({}, status=status.HTTP_200_OK)
