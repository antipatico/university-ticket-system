from rest_framework import serializers
from uts_common.models import *


class OwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_name(self, owner):
        return f"{owner}"

    def get_type(self, owner):
        return "organization" if type(owner) is Organization else "individual"

    class Meta:
        model = Owner
        read_only_fields = fields = ['id', 'name', 'type']


class TicketEventSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = TicketEvent
        read_only_fields = fields = ['id', 'owner', 'status', 'timestamp', 'info']


class TicketSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    tags = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()

    def __init__(self, *args, max_events=None, **kwargs):
        super(TicketSerializer, self).__init__(*args, **kwargs)
        self.max_events = max_events

    def get_tags(self, ticket):
        return [t.tag for t in ticket.tags.all()]

    def get_events(self, ticket):
        events = ticket.events.all().order_by('-timestamp')
        if self.max_events is not None:
            events = events[:self.max_events]
        return TicketEventSerializer(events, many=True).data

    class Meta:
        model = Ticket
        read_only_fields = fields = ['id', 'owner', 'status', 'name', 'description', 'events', 'tags', 'ts_open',
                                     'ts_last_modified', 'ts_closed', 'is_closed']
