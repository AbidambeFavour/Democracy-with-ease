from django.core.management.base import BaseCommand
from django.utils import timezone
from voting.notifications import VotingAlarmSystem
import time


class Command(BaseCommand):
    help = 'Run the voting alarm system to check for active polls and send notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--daemon',
            action='store_true',
            help='Run continuously as a daemon',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Check interval in seconds (default: 60)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Voting Alarm System...'))
        
        if options['daemon']:
            self.run_daemon(options['interval'])
        else:
            self.run_once()

    def run_once(self):
        """Run the alarm system once."""
        self.stdout.write('Checking for newly active polls...')
        
        # Check for newly active polls
        active_count = VotingAlarmSystem.check_and_notify_active_polls()
        if active_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Created notifications for {active_count} newly active polls')
            )
        else:
            self.stdout.write('No newly active polls found.')
        
        # Check for polls ending soon
        ending_count = VotingAlarmSystem.check_ending_polls()
        if ending_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Created reminders for {ending_count} polls ending soon')
            )
        else:
            self.stdout.write('No polls ending soon.')
        
        self.stdout.write(self.style.SUCCESS('Voting alarm check completed.'))

    def run_daemon(self, interval):
        """Run the alarm system continuously as a daemon."""
        self.stdout.write(f'Running voting alarm daemon with {interval}s interval...')
        self.stdout.write('Press Ctrl+C to stop.')
        
        try:
            while True:
                self.stdout.write(f'\n[{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}] Running alarm check...')
                
                # Check for newly active polls
                active_count = VotingAlarmSystem.check_and_notify_active_polls()
                if active_count > 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'  -> Notified {active_count} newly active polls')
                    )
                
                # Check for polls ending soon
                ending_count = VotingAlarmSystem.check_ending_polls()
                if ending_count > 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'  -> Reminded about {ending_count} polls ending soon')
                    )
                
                if active_count == 0 and ending_count == 0:
                    self.stdout.write('  -> No new notifications needed')
                
                self.stdout.write(f'Next check in {interval} seconds...')
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nVoting alarm daemon stopped by user.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in voting alarm daemon: {str(e)}'))
            raise
