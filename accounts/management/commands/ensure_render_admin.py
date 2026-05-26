import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Create or update the initial Render admin user from environment variables.'

    def handle(self, *args, **options):
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '').strip()
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '')
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', '').strip()

        if not email or not password:
            self.stdout.write(
                'Skipping admin creation: DJANGO_SUPERUSER_EMAIL and '
                'DJANGO_SUPERUSER_PASSWORD are not both set.'
            )
            return

        User = get_user_model()
        username = username or email.split('@', 1)[0]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'is_verified': True,
            },
        )

        changed = created
        for field, value in {
            'username': username,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'is_verified': True,
        }.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                changed = True

        if created or os.getenv('DJANGO_SUPERUSER_RESET_PASSWORD', '').lower() in {'1', 'true', 'yes'}:
            user.set_password(password)
            changed = True

        if changed:
            user.save()

        UserProfile.objects.get_or_create(user=user)

        action = 'Created' if created else 'Ensured'
        self.stdout.write(self.style.SUCCESS(f'{action} admin user: {email}'))
