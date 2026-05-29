from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode


def get_site_domain(request=None):
    """Return the best public domain for user-facing email links."""
    if request is not None:
        return request.get_host()

    configured_domain = getattr(settings, 'SITE_DOMAIN', '').strip()
    if configured_domain:
        return configured_domain

    for host in settings.ALLOWED_HOSTS:
        if host and host != '*' and 'onrender.com' not in host:
            return host

    return settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS != ['*'] else 'localhost'


def get_site_scheme(request=None):
    if request is not None and request.is_secure():
        return 'https'
    return getattr(settings, 'SITE_SCHEME', 'https')


def build_absolute_url(path, request=None):
    return f'{get_site_scheme(request)}://{get_site_domain(request)}{path}'


def send_password_reset_email(user, request=None, initiated_by=None):
    """Send a password reset link to a user."""
    uid = urlsafe_base64_encode(force_str(user.pk).encode())
    token = default_token_generator.make_token(user)
    reset_path = reverse(
        'accounts:password_reset_confirm',
        kwargs={'uidb64': uid, 'token': token},
    )
    reset_url = build_absolute_url(reset_path, request)
    domain = get_site_domain(request)
    subject = f'Password reset on {domain}'
    intro = 'A password reset was requested for your SimpleVote account.'
    if initiated_by:
        intro = f'A password reset was sent by {initiated_by.get_full_name() or initiated_by.username}.'

    body = (
        f'Hello {user.get_full_name() or user.username},\n\n'
        f'{intro}\n\n'
        f'Open this link to choose a new password:\n'
        f'{reset_url}\n\n'
        f'If you did not expect this, you can safely ignore this email.\n\n'
        f'Thanks,\n'
        f'SimpleVote'
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return reset_url


def send_activity_email(activity):
    """Email a user about an activity recorded on their account."""
    user = activity.user
    if not getattr(settings, 'ACTIVITY_EMAIL_NOTIFICATIONS', True):
        return False
    if not user.email:
        return False

    profile = getattr(user, 'profile', None)
    if profile is not None and not profile.email_notifications:
        return False

    subject = f'SimpleVote activity: {activity.get_activity_type_display()}'
    body = (
        f'Hello {user.get_full_name() or user.username},\n\n'
        f'Activity was recorded on your SimpleVote account:\n\n'
        f'{activity.description}\n\n'
        f'Time: {activity.timestamp:%Y-%m-%d %H:%M %Z}\n\n'
        f'If this was not you, reset your password immediately:\n'
        f'{build_absolute_url(reverse("accounts:password_reset"))}\n\n'
        f'Thanks,\n'
        f'SimpleVote'
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    return True
