from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Landing page
    path('', views.landing_page, name='landing'),
    path('landing/', views.landing_page, name='landing_page'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Profile
    path('profile/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    
    # Password reset (self-contained views — no get_current_site / sites framework call)
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset-complete/', views.password_reset_complete_view, name='password_reset_complete'),
    
    # User voting features
    path('my-votes/', views.my_votes_view, name='my_votes'),
    
    # AJAX endpoints
    path('toggle-online/', views.toggle_online_status, name='toggle_online'),
]
