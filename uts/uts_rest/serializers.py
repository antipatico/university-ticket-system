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

    def __init__(self, *args, max_events=None, list_events=False, **kwargs):
        super(TicketSerializer, self).__init__(*args, **kwargs)
        self.max_events = max_events
        if not list_events:
            self.events = None
            del self.fields["events"]

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        read_only_fields = fields = ['id', 'username', 'email', 'full_name']


class OrganizationSerializer(serializers.ModelSerializer):
    administered = serializers.SerializerMethodField()
    admin = UserSerializer()
    members = UserSerializer(many=True)

    def __init__(self, *args, user=None, **kwargs):
        super(OrganizationSerializer, self).__init__(*args, **kwargs)
        self.user = user
        if user is None:
            self.administered = None
            del self.fields["administered"]

    def get_administered(self, organization):
        return (organization.admin.id == self.user.id) if self.user is not None else False

    class Meta:
        model = Organization
        read_only_fields = fields = ['id', 'admin', 'members', 'name', 'administered']

