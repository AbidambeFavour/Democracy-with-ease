from django.urls import path
from .views import PollListView, PollDetailView, CreatePollView, add_comment, toggle_reaction

app_name = 'voting'

urlpatterns = [
    path('', PollListView.as_view(), name='poll_list'),
    path('poll/<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('create/', CreatePollView.as_view(), name='create_poll'),
    path('poll/<int:poll_id>/comment/', add_comment, name='add_comment'),
    path('poll/<int:poll_id>/react/<str:reaction_type>/', toggle_reaction, name='toggle_reaction'),
]
