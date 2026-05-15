#!/usr/bin/env python
"""
PostgreSQL setup script for SimpleVote Django application.
This script helps set up PostgreSQL database and run migrations.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def setup_database():
    """Set up PostgreSQL database and run migrations."""
    print("🚀 Setting up PostgreSQL for SimpleVote...")
    
    # Add project root to Python path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
    django.setup()
    
    try:
        print("📦 Installing required packages...")
        os.system(f"{sys.executable} -m pip install psycopg2-binary")
        
        print("🗄️ Creating database migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        print("🔄 Applying database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("👤 Creating superuser (optional)...")
        print("Run 'python manage.py createsuperuser' to create an admin user.")
        
        print("✅ PostgreSQL setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Make sure PostgreSQL is running on your system")
        print("2. Create a database named 'simplevote_db' in PostgreSQL")
        print("3. Update database credentials in settings.py if needed")
        print("4. Run 'python manage.py runserver' to start the application")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        print("\n🔧 Manual setup required:")
        print("1. Install PostgreSQL on your system")
        print("2. Create database: CREATE DATABASE simplevote_db;")
        print("3. Install psycopg2-binary: pip install psycopg2-binary")
        print("4. Run migrations: python manage.py migrate")
        return False
    
    return True

def create_database_sql():
    """Return SQL commands to create the database."""
    return """
-- Connect to PostgreSQL as superuser and run these commands:

-- Create database
CREATE DATABASE simplevote_db;

-- Create user (optional, you can use existing postgres user)
CREATE USER simplevote_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE simplevote_db TO simplevote_user;

-- Connect to the database and grant schema privileges
\\c simplevote_db
GRANT ALL ON SCHEMA public TO simplevote_user;
"""

if __name__ == '__main__':
    print("=" * 50)
    print("SimpleVote PostgreSQL Setup")
    print("=" * 50)
    
    print("\n📋 Prerequisites:")
    print("1. PostgreSQL must be installed and running")
    print("2. Database 'simplevote_db' should exist")
    print("3. User 'postgres' should have privileges")
    
    print("\n🔧 SQL commands to create database:")
    print(create_database_sql())
    
    print("\n" + "=" * 50)
    
    # Try to run setup
    if setup_database():
        print("\n🎉 Setup completed! You can now run the application.")
    else:
        print("\n⚠️ Please complete the manual setup steps above.")
