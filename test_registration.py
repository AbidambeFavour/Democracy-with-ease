#!/usr/bin/env python
"""
Test registration functionality for SimpleVote.
"""

import os
import sys
import django

# Add project to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm

User = get_user_model()

def test_registration_form():
    """Test the registration form directly."""
    print("🧪 Testing Registration Form...")
    
    # Test form validation
    form_data = {
        'username': 'testuser123',
        'email': 'testuser123@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password1': 'complexpassword123',
        'password2': 'complexpassword123',
    }
    
    form = CustomUserCreationForm(data=form_data)
    
    if form.is_valid():
        print("✅ Form is valid!")
        user = form.save()
        print(f"✅ User created: {user.username}")
        
        # Test authentication
        from django.contrib.auth import authenticate
        auth_user = authenticate(username='testuser123', password='complexpassword123')
        if auth_user:
            print("✅ User can authenticate!")
            return True
        else:
            print("❌ User authentication failed")
            return False
    else:
        print("❌ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
        return False

def test_registration_view():
    """Test the registration view via HTTP."""
    print("\n🌐 Testing Registration View...")
    
    client = Client()
    
    # Test GET request
    response = client.get('/accounts/register/')
    if response.status_code == 200:
        print("✅ Registration page loads (GET 200)")
    else:
        print(f"❌ Registration page failed: {response.status_code}")
        return False
    
    # Test POST request
    form_data = {
        'username': 'webtestuser',
        'email': 'webtest@example.com',
        'first_name': 'Web',
        'last_name': 'Test',
        'password1': 'webtestpass123',
        'password2': 'webtestpass123',
    }
    
    response = client.post('/accounts/register/', data=form_data)
    
    if response.status_code == 302:  # Redirect after successful registration
        print("✅ Registration successful (POST 302)")
        
        # Check if user was created
        if User.objects.filter(username='webtestuser').exists():
            print("✅ User created in database!")
            return True
        else:
            print("❌ User not found in database")
            return False
    else:
        print(f"❌ Registration failed: {response.status_code}")
        if response.context and 'form' in response.context:
            form = response.context['form']
            for field, errors in form.errors.items():
                print(f"   {field}: {errors}")
        return False

def cleanup_test_users():
    """Clean up test users."""
    test_usernames = ['testuser123', 'webtestuser']
    for username in test_usernames:
        if User.objects.filter(username=username).exists():
            User.objects.filter(username=username).delete()
            print(f"🧹 Cleaned up test user: {username}")

if __name__ == '__main__':
    print("🚀 Testing Registration Functionality")
    print("=" * 50)
    
    try:
        # Test form directly
        form_works = test_registration_form()
        
        # Test view via HTTP
        view_works = test_registration_view()
        
        if form_works and view_works:
            print("\n🎉 All registration tests passed!")
        else:
            print("\n❌ Some tests failed")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        cleanup_test_users()
        print("\n✅ Test completed")
