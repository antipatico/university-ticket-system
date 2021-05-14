from django.core.management.base import BaseCommand, CommandError
from uts_common.models import *
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Create scheduled jobs, which will be run using django-q qcluster'

    def handle(self, *args, **options):
        from django_q.models import Schedule
        if not Schedule.objects.filter(name="delete_unused_ticket_event_attachments").exists():
            Schedule.objects.create(
                name="delete_unused_ticket_event_attachments",
                func='uts_scheduler.schedules.delete_unused_ticket_event_attachments',
                schedule_type=Schedule.CRON,
                cron="0 3 * * * *",  # Schedule every day at 3 A.M.
            )
