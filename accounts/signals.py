from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from .email_utils import send_activity_email
from .models import User, UserActivity, UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=UserActivity)
def email_user_activity(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_activity_email(instance))
