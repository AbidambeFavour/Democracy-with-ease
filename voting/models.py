from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Category for organizing polls."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Poll(models.Model):
    """Model for a voting poll."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    allow_multiple_votes = models.BooleanField(default=False)
    max_votes_per_user = models.IntegerField(default=1)
    show_results_immediately = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_active(self):
        """Check if the poll is currently active."""
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def is_closed(self):
        """Check if the poll has closed."""
        return timezone.now() > self.end_date

    def has_started(self):
        """Check if the poll has started."""
        return timezone.now() >= self.start_date

    def get_status(self):
        """Get the status of the poll."""
        now = timezone.now()
        # Simple time comparison without timezone complexity
        try:
            if self.start_date and self.end_date:
                # Use small buffer (30 seconds) only for start time to handle minor sync issues
                # No buffer for end time - polls should close exactly when they should
                start_buffer = timedelta(seconds=30)
                if now < self.start_date - start_buffer:
                    return "Upcoming"
                elif self.start_date - start_buffer <= now <= self.end_date:
                    return "Active"
                else:
                    return "Closed"
            else:
                return "Active"  # Default to active if no times set
        except Exception:
            return "Active"  # Default to active on any error

    def get_time_display(self):
        """Get human-readable time display (e.g., '2 days left', '3 hours ago')."""
        now = timezone.now()
        try:
            if self.start_date and self.end_date:
                # Log for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"get_time_display - Poll: {self.title}")
                logger.info(f"  now: {now}")
                logger.info(f"  start_date: {self.start_date}")
                logger.info(f"  end_date: {self.end_date}")
                
                if now < self.start_date:
                    # Time until start
                    delta = self.start_date - now
                    logger.info(f"  Time until start: {delta.total_seconds()} seconds")
                    return self._format_timedelta(delta, "left")
                elif now > self.end_date:
                    # Time since end
                    delta = now - self.end_date
                    logger.info(f"  Time since end: {delta.total_seconds()} seconds")
                    return self._format_timedelta(delta, "ago")
                else:
                    # Time until end
                    delta = self.end_date - now
                    logger.info(f"  Time until end: {delta.total_seconds()} seconds")
                    return self._format_timedelta(delta, "left")
            else:
                return "No time limit"
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in get_time_display: {e}")
            return "No time limit"

    def _format_timedelta(self, delta, suffix):
        """Format timedelta into human-readable string."""
        total_seconds = int(delta.total_seconds())
        if total_seconds < 60:
            return f"{total_seconds} seconds {suffix}"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} {suffix}"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} {suffix}"
        else:
            days = total_seconds // 86400
            return f"{days} day{'s' if days != 1 else ''} {suffix}"

    def get_total_votes(self):
        """Get the total number of votes for this poll."""
        return Vote.objects.filter(poll=self).count()

    def get_results(self):
        """Get the voting results as a dictionary."""
        results = {}
        choices = self.choices.all()
        for choice in choices:
            results[choice] = Vote.objects.filter(choice=choice).count()
        return results

    def get_tags_list(self):
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def can_user_vote(self, user):
        """Check if a user can vote in this poll."""
        if not self.is_active():
            return False, "Poll is not active"
        
        if not self.is_public and user != self.creator:
            return False, "This is a private poll"
        
        vote_count = Vote.objects.filter(poll=self, voter=user).count()
        if vote_count >= self.max_votes_per_user:
            return False, "You have already voted the maximum number of times"
        
        return True, "You can vote"

    def clean(self):
        """Validate model fields."""
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date.')
        
        if self.max_votes_per_user < 1:
            raise ValidationError('Maximum votes per user must be at least 1.')


class Choice(models.Model):
    """Model for a choice in a poll."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.choice_text

    def get_vote_count(self):
        """Get the number of votes for this choice."""
        return Vote.objects.filter(choice=self).count()

    def get_vote_percentage(self):
        """Get the percentage of votes for this choice."""
        total_votes = self.poll.get_total_votes()
        if total_votes == 0:
            return 0
        return (self.get_vote_count() / total_votes) * 100


class Vote(models.Model):
    """Model for a vote on a poll."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-voted_at']

    def __str__(self):
        return f"Vote for {self.choice.choice_text} in {self.poll.title}"


class PollComment(models.Model):
    """Comments on polls."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.poll.title}"


class PollReaction(models.Model):
    """Reactions to polls (like, dislike, etc.)."""
    REACTION_TYPES = [
        ('like', '👍 Like'),
        ('dislike', '👎 Dislike'),
        ('love', '❤️ Love'),
        ('laugh', '😄 Laugh'),
        ('wow', '😮 Wow'),
    ]
    
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['poll', 'user', 'reaction_type']

    def __str__(self):
        return f"{self.user.username} {self.reaction_type} {self.poll.title}"


class UserNotification(models.Model):
    """Notifications for users about poll events."""
    NOTIFICATION_TYPES = [
        ('voting_alarm', 'Voting Alarm'),
        ('ending_reminder', 'Ending Reminder'),
        ('poll_created', 'New Poll'),
        ('poll_closed', 'Poll Closed'),
        ('vote_received', 'Vote Received'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'created_at']),
            models.Index(fields=['notification_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
