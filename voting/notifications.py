from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Poll, UserNotification
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class VotingAlarmSystem:
    """System to manage voting alarms and notifications."""
    
    @staticmethod
    def check_and_notify_active_polls():
        """Check for newly active polls and send notifications."""
        now = timezone.now()
        
        # Find polls that just became active (within the last 5 minutes)
        recent_active_time = now - timezone.timedelta(minutes=5)
        
        newly_active_polls = Poll.objects.filter(
            start_date__gte=recent_active_time,
            start_date__lte=now,
            is_public=True
        ).select_related('creator', 'category')
        
        for poll in newly_active_polls:
            VotingAlarmSystem.send_voting_alarm(poll)
        
        return newly_active_polls.count()
    
    @staticmethod
    def send_voting_alarm(poll):
        """Send voting alarm for a specific poll."""
        try:
            # Get all logged-in users who haven't been notified about this poll
            notified_users = UserNotification.objects.filter(
                poll=poll,
                notification_type='voting_alarm'
            ).values_list('user_id', flat=True)
            
            # Get all active users (online in last 5 minutes)
            active_time = timezone.now() - timezone.timedelta(minutes=5)
            active_users = User.objects.filter(
                last_seen__gte=active_time,
                is_active=True
            ).exclude(id__in=notified_users)
            
            # Create notifications for each active user
            notifications_created = 0
            for user in active_users:
                notification = UserNotification.objects.create(
                    user=user,
                    poll=poll,
                    notification_type='voting_alarm',
                    title=f'Voting Time: {poll.title}',
                    message=f'The poll "{poll.title}" is now open for voting!',
                    is_read=False
                )
                notifications_created += 1
            
            logger.info(f"Created {notifications_created} voting alarm notifications for poll: {poll.title}")
            return notifications_created
            
        except Exception as e:
            logger.error(f"Error sending voting alarm for poll {poll.id}: {str(e)}")
            return 0
    
    @staticmethod
    def check_ending_polls():
        """Check for polls that are ending soon and send reminders."""
        now = timezone.now()
        
        # Find polls ending in the next 30 minutes
        soon_ending_time = now + timezone.timedelta(minutes=30)
        
        ending_soon_polls = Poll.objects.filter(
            end_date__lte=soon_ending_time,
            end_date__gt=now,
            is_public=True
        ).select_related('creator', 'category')
        
        for poll in ending_soon_polls:
            VotingAlarmSystem.send_ending_reminder(poll)
        
        return ending_soon_polls.count()
    
    @staticmethod
    def send_ending_reminder(poll):
        """Send reminder for polls ending soon."""
        try:
            # Get users who haven't been reminded about this poll ending
            notified_users = UserNotification.objects.filter(
                poll=poll,
                notification_type='ending_reminder'
            ).values_list('user_id', flat=True)
            
            # Get users who can still vote in this poll
            from .models import Vote
            voters = Vote.objects.filter(poll=poll).values_list('voter_id', flat=True)
            
            # Get users who haven't voted yet
            potential_voters = User.objects.filter(
                is_active=True
            ).exclude(id__in=voters).exclude(id__in=notified_users)
            
            notifications_created = 0
            for user in potential_voters:
                notification = UserNotification.objects.create(
                    user=user,
                    poll=poll,
                    notification_type='ending_reminder',
                    title=f'Poll Ending Soon: {poll.title}',
                    message=f'The poll "{poll.title}" is ending soon! Cast your vote now.',
                    is_read=False
                )
                notifications_created += 1
            
            logger.info(f"Created {notifications_created} ending reminders for poll: {poll.title}")
            return notifications_created
            
        except Exception as e:
            logger.error(f"Error sending ending reminder for poll {poll.id}: {str(e)}")
            return 0
