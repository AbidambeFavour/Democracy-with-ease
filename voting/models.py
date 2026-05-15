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
        if not self.has_started():
            return "Upcoming"
        elif self.is_active():
            return "Active"
        else:
            return "Closed"

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
