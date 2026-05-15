from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, UserProfileForm
from .models import UserProfile, UserActivity
from voting.models import Poll, Vote

User = get_user_model()


def register_view(request):
    """User registration view with admin options."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Handle admin registration
            is_staff = request.POST.get('is_staff') == 'on'
            is_superuser = request.POST.get('is_superuser') == 'on'
            
            if is_superuser:
                user.is_staff = True
                user.is_superuser = True
            elif is_staff:
                user.is_staff = True
                user.is_superuser = False
            
            user.save()
            
            # Track activity before login
            activity_type = 'admin_registration' if is_staff else 'registration'
            description = f'User registered as {"Super Admin" if is_superuser else "Admin" if is_staff else "Regular User"}'
            UserActivity.objects.create(
                user=user,
                activity_type=activity_type,
                description=description
            )
            
            # Log the user in after registration using the saved user object
            backend = 'accounts.backends.EmailOrUsernameBackend'  # Use the backend path string
            login(request, user, backend=backend)
            
            role_text = "Super Admin" if is_superuser else "Admin" if is_staff else "User"
            messages.success(request, f'{role_text} account created for {user.username}!')
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user.last_seen = timezone.now()
            user.save(update_fields=['last_seen'])

            UserActivity.objects.create(
                user=user,
                activity_type='login',
                description='User logged in'
            )

            messages.info(request, f'You are now logged in as {user.username}.')
            return redirect('accounts:dashboard')
        messages.error(request, 'Invalid username/email or password.')
    else:
        form = CustomAuthenticationForm(request)
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    # Track activity
    UserActivity.objects.create(
        user=request.user,
        activity_type='logout',
        description='User logged out'
    )
    
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('accounts:landing')


@login_required
def dashboard_view(request):
    """User dashboard with statistics and recent activity."""
    user = request.user
    
    # Get user statistics
    recent_votes = Vote.objects.filter(voter=user).select_related('poll', 'choice').order_by('-voted_at')[:5]
    
    # Get overall statistics
    total_votes_cast = Vote.objects.filter(voter=user).count()
    
    # Get recent activities
    recent_activities = UserActivity.objects.filter(user=user).order_by('-timestamp')[:10]
    
    context = {
        'recent_votes': recent_votes,
        'total_votes_cast': total_votes_cast,
        'recent_activities': recent_activities,
    }
    
    # Add admin-specific data if user is staff
    if user.is_staff:
        polls_created = Poll.objects.filter(creator=user).annotate(
            vote_count=Count('vote')
        ).order_by('-created_at')[:5]
        
        total_polls = Poll.objects.filter(creator=user).count()
        active_polls = Poll.objects.filter(creator=user, end_date__gt=timezone.now()).count()
        
        # Get trending polls (excluding user's own polls)
        trending_polls = Poll.objects.annotate(
            vote_count=Count('vote')
        ).filter(
            end_date__gt=timezone.now(),
            start_date__lte=timezone.now()
        ).exclude(creator=user).order_by('-vote_count')[:5]
        
        context.update({
            'polls_created': polls_created,
            'total_polls': total_polls,
            'active_polls': active_polls,
            'trending_polls': trending_polls,
        })
    else:
        # For regular users, get available polls to vote in
        from voting.models import Poll
        voted_poll_ids = Vote.objects.filter(voter=user).values_list('poll_id', flat=True)
        available_polls = Poll.objects.filter(
            is_public=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).exclude(id__in=voted_polls).select_related('creator', 'category')[:5]
        
        context.update({
            'available_polls': available_polls,
            'active_polls': available_polls.count(),
        })
    
    return render(request, 'accounts/dashboard.html', context)


class ProfileView(DetailView):
    """User profile view."""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Get user's polls
        polls = Poll.objects.filter(creator=user).annotate(
            vote_count=Count('vote')
        ).order_by('-created_at')
        
        # Get user's voting activity
        votes = Vote.objects.filter(voter=user).select_related('poll', 'choice').order_by('-voted_at')[:20]
        
        # Check if viewing own profile
        is_own_profile = self.request.user == user
        
        context.update({
            'polls': polls,
            'votes': votes,
            'is_own_profile': is_own_profile,
            'total_polls': polls.count(),
            'total_votes': Vote.objects.filter(voter=user).count(),
        })
        
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/edit_profile.html'
    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        if 'profile_form' in kwargs:
            context['profile_form'] = kwargs['profile_form']
        elif self.request.POST:
            context['profile_form'] = UserProfileForm(self.request.POST, instance=profile)
        else:
            context['profile_form'] = UserProfileForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid() and profile_form.is_valid():
            return self.forms_valid(form, profile_form)
        return self.forms_invalid(form, profile_form)

    def forms_valid(self, form, profile_form):
        form.save()
        profile_form.save()

        UserActivity.objects.create(
            user=self.request.user,
            activity_type='profile_updated',
            description='User updated their profile'
        )

        messages.success(self.request, 'Your profile has been updated successfully!')
        return redirect(self.get_success_url())

    def forms_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


def landing_page(request):
    """Landing page for non-authenticated users."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    # Get some featured polls for display
    featured_polls = Poll.objects.annotate(
        vote_count=Count('vote')
    ).filter(
        end_date__gt=timezone.now(),
        start_date__lte=timezone.now()
    ).order_by('-vote_count')[:6]
    
    # Get statistics
    total_users = User.objects.count()
    total_polls = Poll.objects.count()
    total_votes = Vote.objects.count()
    
    context = {
        'featured_polls': featured_polls,
        'total_users': total_users,
        'total_polls': total_polls,
        'total_votes': total_votes,
    }
    
    return render(request, 'accounts/landing.html', context)


@login_required
def admin_dashboard_view(request):
    """Admin dashboard view for system administrators."""
    # Check if user is admin (you might want to add proper admin checking)
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('accounts:dashboard')
    
    # Get statistics
    total_users = User.objects.count()
    active_polls = Poll.objects.filter(
        end_date__gt=timezone.now(),
        start_date__lte=timezone.now()
    ).count()
    total_votes = Vote.objects.count()
    
    # Get recent activity
    recent_activities = UserActivity.objects.select_related('user').order_by('-timestamp')[:10]
    
    context = {
        'total_users': total_users,
        'active_polls': active_polls,
        'total_votes': total_votes,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def my_votes_view(request):
    """Display user's voting history and statistics."""
    user = request.user
    
    # Get user's votes with related poll and choice data
    votes = Vote.objects.filter(voter=user).select_related(
        'poll', 'choice', 'poll__creator', 'poll__category'
    ).order_by('-voted_at')
    
    # Calculate voting statistics
    total_votes = votes.count()
    recent_votes = votes[:10]  # Last 10 votes
    
    # Get polls the user hasn't voted in yet
    from voting.models import Poll
    voted_poll_ids = votes.values_list('poll_id', flat=True)
    available_polls = Poll.objects.filter(
        is_public=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).exclude(id__in=voted_polls).select_related('creator', 'category')[:5]
    
    # Voting activity by category
    from django.db.models import Count
    category_stats = votes.values(
        'poll__category__name'
    ).annotate(
        vote_count=Count('id')
    ).order_by('-vote_count')
    
    # Monthly voting trend
    from django.db.models import TruncMonth
    monthly_stats = votes.annotate(
        month=TruncMonth('voted_at')
    ).values('month').annotate(
        vote_count=Count('id')
    ).order_by('month')[:12]
    
    context = {
        'total_votes': total_votes,
        'recent_votes': recent_votes,
        'available_polls': available_polls,
        'category_stats': category_stats,
        'monthly_stats': monthly_stats,
    }
    
    return render(request, 'accounts/my_votes.html', context)


@login_required
def toggle_online_status(request):
    """Toggle user online status via AJAX."""
    if request.method == 'POST':
        request.user.last_seen = timezone.now()
        request.user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
