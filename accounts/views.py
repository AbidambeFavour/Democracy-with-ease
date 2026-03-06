from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
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
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # Track activity
            UserActivity.objects.create(
                user=user,
                activity_type='login',
                description='User registered and logged in'
            )
            
            messages.success(request, f'Account created for {username}!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user.last_seen = timezone.now()
                user.save()
                
                # Track activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description='User logged in'
                )
                
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
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
    return redirect('landing')


@login_required
def dashboard_view(request):
    """User dashboard with statistics and recent activity."""
    user = request.user
    
    # Get user statistics
    polls_created = Poll.objects.filter(creator=user).annotate(
        vote_count=Count('vote')
    ).order_by('-created_at')[:5]
    
    recent_votes = Vote.objects.filter(voter=user).select_related('poll', 'choice').order_by('-voted_at')[:5]
    
    # Get overall statistics
    total_polls = Poll.objects.filter(creator=user).count()
    total_votes_cast = Vote.objects.filter(voter=user).count()
    active_polls = Poll.objects.filter(creator=user, end_date__gt=timezone.now()).count()
    
    # Get recent activities
    recent_activities = UserActivity.objects.filter(user=user).order_by('-timestamp')[:10]
    
    # Get trending polls (excluding user's own polls)
    trending_polls = Poll.objects.annotate(
        vote_count=Count('vote')
    ).filter(
        end_date__gt=timezone.now(),
        start_date__lte=timezone.now()
    ).exclude(creator=user).order_by('-vote_count')[:5]
    
    context = {
        'polls_created': polls_created,
        'recent_votes': recent_votes,
        'total_polls': total_polls,
        'total_votes_cast': total_votes_cast,
        'active_polls': active_polls,
        'recent_activities': recent_activities,
        'trending_polls': trending_polls,
    }
    
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
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = UserProfileForm(self.request.POST, instance=self.request.user.profile)
        else:
            context['profile_form'] = UserProfileForm(instance=self.request.user.profile)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        
        if profile_form.is_valid():
            form.save()
            profile_form.save()
            
            # Track activity
            UserActivity.objects.create(
                user=self.request.user,
                activity_type='profile_updated',
                description='User updated their profile'
            )
            
            messages.success(self.request, 'Your profile has been updated successfully!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


def landing_page(request):
    """Landing page for non-authenticated users."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
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
        return redirect('dashboard')
    
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
def toggle_online_status(request):
    """Toggle user online status via AJAX."""
    if request.method == 'POST':
        request.user.last_seen = timezone.now()
        request.user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
