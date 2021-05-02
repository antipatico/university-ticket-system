from rest_framework import serializers
from uts_common.models import *


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        read_only_fields = fields = ['status', 'owner', 'name', 'description', 'tags', 'ts_open', 'ts_last_modified', 'ts_closed']
