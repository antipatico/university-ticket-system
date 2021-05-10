from django.db.models import Q
from django.shortcuts import get_object_or_404
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
        return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationsView(AuthenticatedViewSet):
    def list(self, request):
        organizations = request.user.organizations.all()
        administered_org = request.user.administered_organizations.all()
        serializer = OrganizationSerializer(administered_org.union(organizations), user=request.user, many=True)
        return Response(serializer.data)
