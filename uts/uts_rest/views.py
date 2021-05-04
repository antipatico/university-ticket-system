from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from uts_common.models import *
from uts_rest.serializers import *
from rest_framework.permissions import IsAuthenticated


class AuthenticatedViewSet(ViewSet):
    permission_classes = [IsAuthenticated]


# Get the 3 most recent tickets the user "interacted with"
class RecentActivitiesView(AuthenticatedViewSet):
    def list(self, request):
        tickets = Ticket.objects.filter(
            Q(owner_id=request.user.individual.id) | Q(subscribers__in=[request.user])).order_by(
            "-ts_last_modified")[:3]
        serializer = TicketSerializer(tickets, max_events=3, list_events=True, many=True)
        return Response(serializer.data)


class TicketsView(AuthenticatedViewSet):
    def list(self, request):
        tickets = Ticket.objects.filter(owner_id=request.user.individual.id).order_by("-ts_open")
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Ticket.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TicketSerializer(user, list_events=True)
        return Response(serializer.data)


class OrganizationsView(AuthenticatedViewSet):
    def list(self, request):
        organizations = request.user.organizations.all()
        administered_org = request.user.administered_organizations.all()
        serializer = OrganizationSerializer(administered_org.union(organizations), user=request.user, many=True)
        return Response(serializer.data)
