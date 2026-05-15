from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Poll, Choice, Vote, Category, PollComment, PollReaction
from accounts.models import UserActivity, UserProfile

User = get_user_model()


def is_super_admin(user):
    """Check if user is a super admin."""
    return user.is_superuser and user.is_staff


@login_required
@user_passes_test(is_super_admin)
def super_admin_dashboard(request):
    """Super admin dashboard with overall system control."""
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Super admin privileges required.")
        return redirect('accounts:dashboard')
    
    # System statistics
    total_users = User.objects.count()
    total_polls = Poll.objects.count()
    total_votes = Vote.objects.count()
    active_polls = Poll.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).count()
    
    # Recent activity
    recent_activities = UserActivity.objects.select_related('user').order_by('-timestamp')[:20]
    recent_polls = Poll.objects.select_related('creator').order_by('-created_at')[:10]
    
    # User statistics
    admin_users = User.objects.filter(is_staff=True).count()
    regular_users = total_users - admin_users
    verified_users = User.objects.filter(is_verified=True).count()
    
    # Poll statistics
    public_polls = Poll.objects.filter(is_public=True).count()
    private_polls = Poll.objects.filter(is_public=False).count()
    
    context = {
        'total_users': total_users,
        'total_polls': total_polls,
        'total_votes': total_votes,
        'active_polls': active_polls,
        'admin_users': admin_users,
        'regular_users': regular_users,
        'verified_users': verified_users,
        'public_polls': public_polls,
        'private_polls': private_polls,
        'recent_activities': recent_activities,
        'recent_polls': recent_polls,
    }
    
    return render(request, 'voting/super_admin_dashboard.html', context)


@login_required
@user_passes_test(is_super_admin)
def manage_polls(request):
    """Super admin poll management."""
    polls = Poll.objects.select_related('creator', 'category').annotate(
        vote_count=Count('vote')
    ).order_by('-created_at')
    
    # Filter options
    status_filter = request.GET.get('status')
    creator_filter = request.GET.get('creator')
    
    if status_filter == 'active':
        polls = polls.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
    elif status_filter == 'closed':
        polls = polls.filter(end_date__lt=timezone.now())
    elif status_filter == 'upcoming':
        polls = polls.filter(start_date__gt=timezone.now())
    
    if creator_filter:
        polls = polls.filter(creator__username__icontains=creator_filter)
    
    context = {
        'polls': polls,
        'status_filter': status_filter,
        'creator_filter': creator_filter,
    }
    
    return render(request, 'voting/manage_polls.html', context)


@login_required
@user_passes_test(is_super_admin)
def delete_poll(request, poll_id):
    """Delete a poll (super admin only)."""
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        poll_title = poll.title
        poll.delete()
        messages.success(request, f"Poll '{poll_title}' has been deleted.")
        return redirect('voting:manage_polls')
    
    return render(request, 'voting/delete_poll.html', {'poll': poll})


@login_required
@user_passes_test(is_super_admin)
def manage_users(request):
    """Super admin user management."""
    users = User.objects.annotate(
        poll_count=Count('created_polls'),
        vote_count=Count('votes')
    ).order_by('-date_joined')
    
    # Filter options
    user_type = request.GET.get('type')
    
    if user_type == 'admin':
        users = users.filter(is_staff=True)
    elif user_type == 'regular':
        users = users.filter(is_staff=False)
    elif user_type == 'verified':
        users = users.filter(is_verified=True)
    
    context = {
        'users': users,
        'user_type': user_type,
    }
    
    return render(request, 'voting/manage_users.html', context)


@login_required
@user_passes_test(is_super_admin)
def toggle_user_status(request, user_id):
    """Toggle user admin status (super admin only)."""
    user = get_object_or_404(User, id=user_id)
    
    if user == request.user:
        messages.error(request, "You cannot modify your own admin status.")
        return redirect('voting:manage_users')
    
    if request.method == 'POST':
        user.is_staff = not user.is_staff
        if user.is_staff:
            user.is_superuser = True  # Make staff users also superusers
            messages.success(request, f"{user.username} is now an administrator.")
        else:
            user.is_superuser = False
            messages.success(request, f"{user.username} is no longer an administrator.")
        user.save()
    
    return redirect('voting:manage_users')


@login_required
@user_passes_test(is_super_admin)
def system_settings(request):
    """Super admin system settings."""
    if request.method == 'POST':
        # Handle system-wide settings
        allow_registrations = request.POST.get('allow_registrations') == 'on'
        require_verification = request.POST.get('require_verification') == 'on'
        
        # Store settings in database or environment variables
        # For now, just show success message
        messages.success(request, "System settings updated successfully.")
    
    context = {
        # Add system settings here
    }
    
    return render(request, 'voting/system_settings.html', context)


@login_required
@user_passes_test(is_super_admin)
def system_logs(request):
    """View system activity logs."""
    activities = UserActivity.objects.select_related('user').order_by('-timestamp')[:100]
    
    # Filter options
    activity_type = request.GET.get('type')
    user_filter = request.GET.get('user')
    
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    if user_filter:
        activities = activities.filter(user__username__icontains=user_filter)
    
    context = {
        'activities': activities,
        'activity_type': activity_type,
        'user_filter': user_filter,
        'activity_types': UserActivity._meta.get_field('activity_type').choices,
    }
    
    return render(request, 'voting/system_logs.html', context)
