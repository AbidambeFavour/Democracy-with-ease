#!/usr/bin/env python
"""
Test dashboard functionality for SimpleVote.
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
from django.urls import reverse

User = get_user_model()

def test_dashboard_access():
    """Test dashboard access after login."""
    print("🧪 Testing Dashboard Access...")
    
    client = Client()
    
    # Try to access dashboard without login (should redirect)
    response = client.get('/accounts/dashboard/')
    if response.status_code == 302:
        print("✅ Dashboard redirects unauthenticated users")
    else:
        print(f"❌ Dashboard should redirect unauthenticated users: {response.status_code}")
        return False
    
    # Login with test user
    login_success = client.login(username='testuser', password='password123')
    if login_success:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return False
    
    # Access dashboard after login
    response = client.get('/accounts/dashboard/')
    if response.status_code == 200:
        print("✅ Dashboard loads successfully for authenticated user")
        
        # Check if template contains expected content
        if 'Welcome back' in response.content.decode():
            print("✅ Dashboard contains welcome message")
        else:
            print("⚠️ Dashboard missing welcome message")
        
        return True
    else:
        print(f"❌ Dashboard failed to load: {response.status_code}")
        if hasattr(response, 'context'):
            print(f"   Context keys: {list(response.context.keys())}")
        return False

def test_dashboard_template():
    """Test dashboard template rendering."""
    print("\n🌐 Testing Dashboard Template...")
    
    client = Client()
    
    # Login first
    client.login(username='testuser', password='password123')
    
    # Test dashboard page
    response = client.get('/accounts/dashboard/')
    
    if response.status_code == 200:
        content = response.content.decode()
        
        # Check for key elements
        checks = [
            ('Welcome back', 'Welcome message'),
            ('polls created', 'Polls count'),
            ('votes cast', 'Votes count'),
            ('Recent Activity', 'Activity section'),
        ]
        
        all_good = True
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description} found")
            else:
                print(f"⚠️ {description} not found")
                all_good = False
        
        return all_good
    else:
        print(f"❌ Template test failed: {response.status_code}")
        return False

if __name__ == '__main__':
    print("🚀 Testing Dashboard Functionality")
    print("=" * 50)
    
    try:
        # Test dashboard access
        access_works = test_dashboard_access()
        
        # Test template rendering
        template_works = test_dashboard_template()
        
        if access_works and template_works:
            print("\n🎉 All dashboard tests passed!")
        else:
            print("\n❌ Some dashboard tests failed")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Dashboard test completed")
