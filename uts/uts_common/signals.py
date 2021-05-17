from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from django_q.tasks import schedule

from uts_common.models import *

# https://docs.djangoproject.com/en/3.1/topics/signals/#connecting-receiver-functions
# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html


@receiver(post_save, sender=User, dispatch_uid="user_post_save")
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Individual.objects.create(user=instance)


@receiver(post_save, sender=TicketEvent, dispatch_uid="ticket_event_post_save")
def ticket_event_post_save(sender, instance, created, **kwargs):
    if created:
        instance.ticket.ts_last_modified = timezone.now()
        instance.ticket.save()
        schedule('uts_scheduler.schedules.send_email_notification',
                 instance.id,
                 schedule_type='O')


@receiver(pre_delete, sender=TicketEventAttachment, dispatch_uid="ticket_event_attachment_pre_delete")
def ticket_event_attachment_pre_delete(sender, instance, using, **kwargs):
    if instance.file:
        instance.file.delete()
