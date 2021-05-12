import logging
from datetime import timedelta
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from uts_common.models import TicketEventAttachment

logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def delete_unused_attachments(max_age=43_200):
    unused_attachments = TicketEventAttachment.objects.filter(event=None, timestamp__lt=timezone.now()-timedelta(hours=12))
    deleted, _ = unused_attachments.delete()
    logger.info(f"delete_unused_attachments: deleted {deleted} unused uploaded files.")


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        logger.addHandler(logging.StreamHandler(self.stdout))
        logger.setLevel(logging.INFO)
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        scheduler.add_job(
            delete_unused_attachments,
            trigger=CronTrigger(
                hour="03", minute="00"
            ),
            id="delete_unused_attachments",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")