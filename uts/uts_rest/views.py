from django.db.models import Q
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from uts_common.models import *
from uts_rest.serializers import TicketSerializer
from rest_framework.permissions import IsAuthenticated


class AuthenticatedViewSet(ViewSet):
    permission_classes = [IsAuthenticated]


# Get the 3 most recent tickets the user "interacted with"
class RecentActivitiesView(AuthenticatedViewSet):
    def list(self, request):
        owners = set([request.user.individual.id] +
                     [o.id for o in request.user.organizations.all()] +
                     [o.id for o in request.user.administered_organizations.all()])
        tickets = Ticket.objects.filter(Q(owner_id__in=owners) | Q(subscribers__in=[request.user])) \
                                .order_by("-ts_last_modified")[:3]
        serializer = TicketSerializer(tickets, max_events=3, many=True)
        return Response(serializer.data)


class TicketsView(AuthenticatedViewSet):
    def list(self, request):
        tickets = Ticket.objects.filter(owner_id=request.user.individual.id).order_by("-ts_open")
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
