from django.apps import AppConfig


class UtsSchedulerConfig(AppConfig):
    name = 'uts_scheduler'

    def ready(self):
        from django_q.models import Schedule
        Schedule.objects.get_or_create(
            name="delete_unused_ticket_event_attachments",
            func='uts_scheduler.schedules.delete_unused_ticket_event_attachments',
            schedule_type=Schedule.CRON,
            cron="0 3 * * * *",  # Schedule every day at 3 A.M.
            repeats=-1
        )
