from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from django.http import Http404
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from .models import Poll, Choice, Vote, Category, PollComment, PollReaction
from accounts.models import UserActivity

User = get_user_model()


class PollListView(ListView):
    """View to display a list of all polls."""
    model = Poll
    template_name = 'voting/poll_list.html'
    context_object_name = 'polls'
    paginate_by = 12

    def get_queryset(self):
        """Return polls with filtering and search capabilities."""
        queryset = Poll.objects.select_related('creator', 'category').annotate(
            vote_count=Count('vote')
        ).order_by('-created_at')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
        elif status == 'closed':
            queryset = queryset.filter(end_date__lt=timezone.now())
        elif status == 'upcoming':
            queryset = queryset.filter(start_date__gt=timezone.now())
        
        # Only show public polls for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True)
        
        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_status'] = self.request.GET.get('status', '')
        return context


class PollDetailView(DetailView):
    """View to display poll details and handle voting."""
    model = Poll
    template_name = 'voting/poll_detail.html'
    context_object_name = 'poll'

    def get_queryset(self):
        """Select related objects for better performance."""
        return Poll.objects.select_related('creator', 'category').prefetch_related(
            'choices', 'comments__author', 'reactions__user'
        )

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        
        # Check if user can vote
        if self.request.user.is_authenticated:
            can_vote, vote_message = poll.can_user_vote(self.request.user)
            has_voted = Vote.objects.filter(
                poll=poll, 
                voter=self.request.user
            ).exists()
            
            # Get user's reaction
            user_reaction = PollReaction.objects.filter(
                poll=poll, 
                user=self.request.user
            ).first()
        else:
            can_vote = False
            vote_message = "Please login to vote"
            has_voted = False
            user_reaction = None
        
        # Get results if poll is closed or show_immediately is True
        show_results = poll.is_closed() or poll.show_results_immediately
        if show_results:
            results = poll.get_results()
        else:
            results = None
        
        # Get reactions count
        reactions_count = {}
        for reaction_type, _ in PollReaction.REACTION_TYPES:
            reactions_count[reaction_type] = PollReaction.objects.filter(
                poll=poll, 
                reaction_type=reaction_type
            ).count()
        
        context.update({
            'can_vote': can_vote,
            'vote_message': vote_message,
            'has_voted': has_voted,
            'results': results,
            'show_results': show_results,
            'user_reaction': user_reaction,
            'reactions_count': reactions_count,
            'comments': poll.comments.select_related('author').all(),
        })
        
        return context

    def post(self, request, *args, **kwargs):
        """Handle voting form submission."""
        if not request.user.is_authenticated:
            messages.error(request, "Please login to vote.")
            return redirect('accounts:login')
        
        poll = self.get_object()
        
        # Check if user can vote
        can_vote, vote_message = poll.can_user_vote(request.user)
        if not can_vote:
            messages.error(request, vote_message)
            return redirect('voting:poll_detail', pk=poll.pk)
        
        # Get selected choice
        choice_id = request.POST.get('choice')
        if not choice_id:
            messages.error(request, "Please select a choice.")
            return redirect('voting:poll_detail', pk=poll.pk)
        
        try:
            choice = Choice.objects.get(id=choice_id, poll=poll)
        except Choice.DoesNotExist:
            messages.error(request, "Invalid choice.")
            return redirect('voting:poll_detail', pk=poll.pk)
        
        # Create the vote
        try:
            Vote.objects.create(
                poll=poll,
                choice=choice,
                voter=request.user,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Track activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='vote_cast',
                description=f'Voted in poll: {poll.title}',
                related_poll=poll
            )
            
            messages.success(request, "Your vote has been recorded!")
        except IntegrityError:
            messages.error(request, "You have already voted in this poll.")
        
        return redirect('voting:poll_detail', pk=poll.pk)


class CreatePollView(LoginRequiredMixin, View):
    """View to create a new poll."""
    template_name = 'voting/create_poll.html'

    def get(self, request):
        """Display the poll creation form."""
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        """Handle poll creation form submission."""
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        tags = request.POST.get('tags', '')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        
        # Advanced options
        is_public = request.POST.get('is_public') == 'on'
        allow_multiple_votes = request.POST.get('allow_multiple_votes') == 'on'
        max_votes_per_user = int(request.POST.get('max_votes_per_user', 1))
        show_results_immediately = request.POST.get('show_results_immediately') == 'on'
        
        # Get choices
        choice_texts = []
        i = 1
        while f'choice_{i}' in request.POST:
            choice_text = request.POST.get(f'choice_{i}').strip()
            if choice_text:
                choice_texts.append(choice_text)
            i += 1
        
        # Validate required fields
        if not title:
            messages.error(request, "Poll title is required.")
            return self.get(request)
        
        if len(choice_texts) < 2:
            messages.error(request, "At least two choices are required.")
            return self.get(request)
        
        # Parse datetime fields
        try:
            start_datetime = timezone.datetime.strptime(
                f"{start_date} {start_time}", 
                "%Y-%m-%d %H:%M"
            )
            end_datetime = timezone.datetime.strptime(
                f"{end_date} {end_time}", 
                "%Y-%m-%d %H:%M"
            )
            # Make timezone-aware
            start_datetime = timezone.make_aware(start_datetime)
            end_datetime = timezone.make_aware(end_datetime)
        except (ValueError, TypeError):
            messages.error(request, "Invalid date or time format.")
            return self.get(request)
        
        # Validate dates
        if end_datetime <= start_datetime:
            messages.error(request, "End date/time must be after start date/time.")
            return self.get(request)
        
        # Create poll
        try:
            poll = Poll.objects.create(
                title=title,
                description=description,
                creator=request.user,
                category_id=category_id if category_id else None,
                tags=tags,
                start_date=start_datetime,
                end_date=end_datetime,
                is_public=is_public,
                allow_multiple_votes=allow_multiple_votes,
                max_votes_per_user=max_votes_per_user,
                show_results_immediately=show_results_immediately
            )
            
            # Create choices
            for choice_text in choice_texts:
                Choice.objects.create(
                    poll=poll,
                    choice_text=choice_text
                )
            
            # Track activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='poll_created',
                description=f'Created poll: {poll.title}',
                related_poll=poll
            )
            
            messages.success(request, f"Poll '{title}' created successfully!")
            return redirect('voting:poll_detail', pk=poll.pk)
            
        except Exception as e:
            messages.error(request, f"Error creating poll: {str(e)}")
            return self.get(request)


@login_required
def add_comment(request, poll_id):
    """Add a comment to a poll."""
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            PollComment.objects.create(
                poll=poll,
                author=request.user,
                content=content
            )
            messages.success(request, "Comment added successfully!")
    
    return redirect('voting:poll_detail', pk=poll_id)


@login_required
def toggle_reaction(request, poll_id, reaction_type):
    """Toggle reaction on a poll."""
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Validate reaction type
    valid_reactions = [r[0] for r in PollReaction.REACTION_TYPES]
    if reaction_type not in valid_reactions:
        return redirect('voting:poll_detail', pk=poll_id)
    
    # Check if user already has this reaction
    existing_reaction = PollReaction.objects.filter(
        poll=poll, 
        user=request.user, 
        reaction_type=reaction_type
    ).first()
    
    if existing_reaction:
        existing_reaction.delete()
    else:
        # Remove any existing reactions from this user on this poll
        PollReaction.objects.filter(poll=poll, user=request.user).delete()
        # Add new reaction
        PollReaction.objects.create(
            poll=poll,
            user=request.user,
            reaction_type=reaction_type
        )
    
    return redirect('voting:poll_detail', pk=poll_id)
