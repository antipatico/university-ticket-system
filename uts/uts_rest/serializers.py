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


class TicketEventAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEventAttachment
        read_only_fields = fields = ['id', 'name', 'file']


class TicketEventSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    attachments = TicketEventAttachmentsSerializer(many=True)

    class Meta:
        model = TicketEvent
        read_only_fields = fields = ['id', 'owner', 'status', 'timestamp', 'info', 'attachments']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = fields = ['id', 'username', 'email', 'full_name']


class TicketSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    tags = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    subscribers = UserSerializer(many=True)
    is_owned = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def __init__(self, *args, max_events=None, list_events=False, user=None, **kwargs):
        super(TicketSerializer, self).__init__(*args, **kwargs)
        self.max_events = max_events
        if not list_events:
            self.events = None
            del self.fields["events"]
        if user is None:
            self.is_owned = None
            self.is_subscribed = None
            del self.fields["is_owned"]
            del self.fields["is_subscribed"]
        self.user = user

    def get_tags(self, ticket):
        return [t.tag for t in ticket.tags.all()]

    def get_events(self, ticket):
        events = ticket.events.all().order_by('-timestamp')
        if self.max_events is not None:
            events = events[:self.max_events]
        return TicketEventSerializer(events, many=True).data

    def get_is_owned(self, ticket):
        return ticket.is_owned_by(self.user.individual)

    def get_is_subscribed(self, ticket):
        return self.user in ticket.subscribers.all()

    class Meta:
        model = Ticket
        read_only_fields = fields = ['id', 'owner', 'status', 'name', 'description', 'events', 'tags', 'ts_open',
                                     'ts_last_modified', 'ts_closed', 'is_closed', 'is_owned', 'is_subscribed',
                                     'subscribers']


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


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEventAttachment
        read_only_fields = fields = ['id', 'name', 'file']
