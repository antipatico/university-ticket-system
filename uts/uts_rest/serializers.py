from rest_framework import serializers
from uts_common.models import *


class OwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    type = serializers.SerializerMethodField('get_type')

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
    tags = serializers.SerializerMethodField('get_tags')
    events = TicketEventSerializer(many=True)

    def get_tags(self, ticket):
        return [t.tag for t in ticket.tags.all()]

    class Meta:
        model = Ticket
        read_only_fields = fields = ['id', 'owner', 'status', 'name', 'description', 'events', 'tags', 'ts_open',
                                     'ts_last_modified', 'ts_closed', 'is_closed']
