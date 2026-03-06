from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with additional fields."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'last_seen', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_verified', 'created_at', 'last_seen']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'avatar', 
                                      'date_of_birth', 'location', 'website', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_seen', 'created_at')}),
    )
    
    readonly_fields = ['created_at', 'last_seen']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    def get_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "No avatar"
    get_avatar.short_description = 'Avatar'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin."""
    list_display = ['user', 'email_notifications', 'push_notifications', 'public_profile', 'theme', 'language']
    list_filter = ['email_notifications', 'push_notifications', 'public_profile', 'theme', 'language']
    search_fields = ['user__username', 'user__email']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """User activity admin."""
    list_display = ['user', 'activity_type', 'description', 'timestamp', 'related_poll']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'description']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    def get_related_poll(self, obj):
        if obj.related_poll:
            return obj.related_poll.title
        return "N/A"
    get_related_poll.short_description = 'Related Poll'
