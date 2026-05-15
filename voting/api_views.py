from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from .models import Poll, UserNotification
import json

User = get_user_model()


@login_required
@require_http_methods(["GET"])
def get_notifications(request):
    """Get unread notifications for the current user."""
    notifications = UserNotification.objects.filter(
        user=request.user,
        is_read=False
    ).select_related('poll').order_by('-created_at')[:10]
    
    notification_data = []
    for notification in notifications:
        notif_data = {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'created_at': notification.created_at.isoformat(),
            'poll_id': notification.poll.id if notification.poll else None,
            'poll_title': notification.poll.title if notification.poll else None,
        }
        notification_data.append(notif_data)
    
    return JsonResponse({
        'notifications': notification_data,
        'unread_count': notifications.count()
    })


@login_required
@require_http_methods(["POST"])
def mark_notification_read(request):
    """Mark a notification as read."""
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        notification = UserNotification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'success': True})
    except (UserNotification.DoesNotExist, json.JSONDecodeError):
        return JsonResponse({'success': False}, status=400)


@login_required
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read for the current user."""
    UserNotification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["GET"])
def check_active_polls(request):
    """Check for polls that are currently active and available for voting."""
    now = timezone.now()
    
    # Get polls the user can vote in
    available_polls = Poll.objects.filter(
        start_date__lte=now,
        end_date__gte=now,
        is_public=True
    ).annotate(
        vote_count=Count('vote')
    ).select_related('creator', 'category')
    
    # Filter polls the user hasn't voted in yet
    if request.user.is_authenticated:
        from .models import Vote
        voted_polls = Vote.objects.filter(voter=request.user).values_list('poll_id', flat=True)
        available_polls = available_polls.exclude(id__in=voted_polls)
    
    poll_data = []
    for poll in available_polls[:5]:  # Limit to 5 most recent
        poll_data.append({
            'id': poll.id,
            'title': poll.title,
            'description': poll.description[:100] if poll.description else '',
            'category': poll.category.name if poll.category else 'General',
            'vote_count': poll.vote_count,
            'created_at': poll.created_at.isoformat(),
            'end_date': poll.end_date.isoformat(),
        })
    
    return JsonResponse({
        'available_polls': poll_data,
        'count': len(poll_data)
    })


@login_required
@require_http_methods(["GET"])
def notification_settings(request):
    """Get user notification preferences."""
    # For now, return default settings
    # In a full implementation, this would come from user profile
    return JsonResponse({
        'voting_alarms': True,
        'ending_reminders': True,
        'sound_enabled': True,
        'popup_enabled': True,
    })


@login_required
@require_http_methods(["POST"])
def update_notification_settings(request):
    """Update user notification preferences."""
    try:
        data = json.loads(request.body)
        
        # For now, just return success
        # In a full implementation, this would save to user profile
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'success': False}, status=400)
