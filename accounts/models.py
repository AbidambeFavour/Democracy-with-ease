from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom user model with additional fields."""
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"https://ui-avatars.com/api/?name={self.get_full_name()}&background=0d6efd&color=fff&size=150"
    
    def is_online(self):
        """Check if user is online (last seen within 5 minutes)."""
        return (timezone.now() - self.last_seen).total_seconds() < 300
    
    def get_polls_created_count(self):
        """Get number of polls created by user."""
        from voting.models import Poll
        return Poll.objects.filter(creator=self).count()
    
    def get_votes_cast_count(self):
        """Get number of votes cast by user."""
        from voting.models import Vote
        return Vote.objects.filter(voter=self).count()


class UserProfile(models.Model):
    """Extended user profile with preferences and settings."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    show_real_name = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto')
    ], default='light')
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserActivity(models.Model):
    """Track user activities for analytics and notifications."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=[
        ('poll_created', 'Poll Created'),
        ('vote_cast', 'Vote Cast'),
        ('poll_ended', 'Poll Ended'),
        ('profile_updated', 'Profile Updated'),
        ('login', 'Login'),
        ('logout', 'Logout')
    ])
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    related_poll = models.ForeignKey('voting.Poll', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['activity_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.activity_type} at {self.timestamp}"
