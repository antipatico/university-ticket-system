from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

# https://docs.djangoproject.com/en/3.1/topics/signals/#connecting-receiver-functions
# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html


@receiver(post_save, sender=User, dispatch_uid="user_profile_post_save")
def user_profile_post_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
