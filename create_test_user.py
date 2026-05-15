#!/usr/bin/env python
"""
Create test user for SimpleVote application.
"""

import os
import sys
import django

# Add project root to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()

def create_test_users():
    """Create test users for testing the application."""
    
    # Test user 1
    if not User.objects.filter(username='testuser').exists():
        user1 = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        UserProfile.objects.create(user=user1)
        print("✅ Created test user: testuser / password123")
    else:
        print("ℹ️ Test user 'testuser' already exists")
    
    # Test user 2
    if not User.objects.filter(username='voter').exists():
        user2 = User.objects.create_user(
            username='voter',
            email='voter@example.com',
            password='password123',
            first_name='Regular',
            last_name='Voter'
        )
        UserProfile.objects.create(user=user2)
        print("✅ Created test user: voter / password123")
    else:
        print("ℹ️ Test user 'voter' already exists")
    
    # Admin user check
    if User.objects.filter(username='admin').exists():
        admin = User.objects.get(username='admin')
        print(f"ℹ️ Admin user exists: {admin.email}")
    else:
        print("ℹ️ Admin user not found")
    
    print("\n📋 Available test users:")
    print("1. testuser / password123")
    print("2. voter / password123")
    print("3. (Check if admin exists)")

if __name__ == '__main__':
    print("🚀 Creating test users for SimpleVote...")
    create_test_users()
    print("\n✅ Test user setup completed!")
