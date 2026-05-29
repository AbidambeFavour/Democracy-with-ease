from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
import logging

from .email_utils import send_activity_email
from .models import User, UserActivity, UserProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=UserActivity)
def email_user_activity(sender, instance, created, **kwargs):
    # Temporarily disabled to prevent SMTP connection failures from breaking login
    # Re-enable once SMTP is properly configured and tested
    return


def _send_activity_email_safely(activity):
    try:
        send_activity_email(activity)
    except Exception:
        logger.exception('Activity email failed for activity %s', activity.pk)
