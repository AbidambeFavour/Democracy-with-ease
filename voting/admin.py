from django.contrib import admin
from .models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
    """Inline admin for choices in poll admin."""
    model = Choice
    extra = 2  # Show 2 empty choice fields by default
    min_num = 2  # Require at least 2 choices


class VoteInline(admin.TabularInline):
    """Inline admin for votes in poll admin."""
    model = Vote
    extra = 0
    readonly_fields = ('voter_identifier', 'voted_at')
    can_delete = False


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Admin configuration for Poll model."""
    list_display = ['title', 'get_status', 'start_date', 'end_date', 'get_total_votes', 'created_at']
    list_filter = ['start_date', 'end_date', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'get_total_votes_display']
    inlines = [ChoiceInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Timing', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('created_at', 'get_total_votes_display'),
            'classes': ('collapse',)
        }),
    )
    
    def get_total_votes_display(self, obj):
        """Display total votes in admin."""
        return obj.get_total_votes()
    get_total_votes_display.short_description = 'Total Votes'
    
    def get_total_votes(self, obj):
        """Display total votes in list view."""
        return obj.get_total_votes()
    get_total_votes.short_description = 'Votes'
    
    def get_status(self, obj):
        """Display poll status with color coding."""
        status = obj.get_status()
        if status == 'Active':
            return '🟢 Active'
        elif status == 'Closed':
            return '🔴 Closed'
        else:
            return '🟡 Upcoming'
    get_status.short_description = 'Status'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Choice model."""
    list_display = ['choice_text', 'poll', 'get_vote_count', 'get_vote_percentage']
    list_filter = ['poll']
    search_fields = ['choice_text', 'poll__title']
    readonly_fields = ['get_vote_count_display', 'get_vote_percentage_display']
    
    def get_vote_count(self, obj):
        """Display vote count in list view."""
        return obj.get_vote_count()
    get_vote_count.short_description = 'Votes'
    
    def get_vote_percentage(self, obj):
        """Display vote percentage in list view."""
        return f"{obj.get_vote_percentage():.1f}%"
    get_vote_percentage.short_description = 'Percentage'
    
    def get_vote_count_display(self, obj):
        """Display vote count in detail view."""
        return obj.get_vote_count()
    get_vote_count_display.short_description = 'Vote Count'
    
    def get_vote_percentage_display(self, obj):
        """Display vote percentage in detail view."""
        return f"{obj.get_vote_percentage():.1f}%"
    get_vote_percentage_display.short_description = 'Vote Percentage'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin configuration for Vote model."""
    list_display = ['poll', 'choice', 'voter', 'voted_at', 'ip_address']
    list_filter = ['poll', 'voted_at']
    search_fields = ['poll__title', 'choice__choice_text', 'voter__username', 'voter__email']
    readonly_fields = ['voted_at']
    
    fieldsets = (
        (None, {
            'fields': ('poll', 'choice', 'voter')
        }),
        ('Additional Information', {
            'fields': ('ip_address', 'voted_at')
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition of votes through admin."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing of votes through admin."""
        return False
