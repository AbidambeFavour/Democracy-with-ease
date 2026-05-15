from django.urls import path
from .views import PollListView, PollDetailView, CreatePollView, add_comment, toggle_reaction
from . import admin_views, api_views

app_name = 'voting'

urlpatterns = [
    # Public voting URLs
    path('', PollListView.as_view(), name='poll_list'),
    path('poll/<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('create/', CreatePollView.as_view(), name='create_poll'),
    path('poll/<int:poll_id>/comment/', add_comment, name='add_comment'),
    path('poll/<int:poll_id>/react/<str:reaction_type>/', toggle_reaction, name='toggle_reaction'),
    
    # Super admin URLs
    path('admin/dashboard/', admin_views.super_admin_dashboard, name='super_admin_dashboard'),
    path('admin/manage-polls/', admin_views.manage_polls, name='manage_polls'),
    path('admin/delete-poll/<int:poll_id>/', admin_views.delete_poll, name='delete_poll'),
    path('admin/manage-users/', admin_views.manage_users, name='manage_users'),
    path('admin/toggle-user/<int:user_id>/', admin_views.toggle_user_status, name='toggle_user_status'),
    path('admin/settings/', admin_views.system_settings, name='system_settings'),
    path('admin/logs/', admin_views.system_logs, name='system_logs'),
    
    # API URLs for notifications
    path('api/notifications/', api_views.get_notifications, name='get_notifications'),
    path('api/notifications/read/', api_views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/read-all/', api_views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/active-polls/', api_views.check_active_polls, name='check_active_polls'),
    path('api/notification-settings/', api_views.notification_settings, name='notification_settings'),
    path('api/notification-settings/update/', api_views.update_notification_settings, name='update_notification_settings'),
]
