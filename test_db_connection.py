#!/usr/bin/env python
"""
Test PostgreSQL connection for SimpleVote.
"""

import os
import sys

def test_connection():
    """Test database connection with current settings."""
    try:
        import django
        from django.conf import settings
        from django.db import connection
        
        # Add project to path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, BASE_DIR)
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
        django.setup()
        
        # Test connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result == (1,):
                    print("✅ Database connection successful!")
                    print(f"📊 Database: {settings.DATABASES['default']['NAME']}")
                    print(f"👤 User: {settings.DATABASES['default']['USER']}")
                    print(f"🌐 Host: {settings.DATABASES['default']['HOST']}")
                    return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print(f"📊 Database: {settings.DATABASES['default']['NAME']}")
            print(f"👤 User: {settings.DATABASES['default']['USER']}")
            print(f"🔐 Password: {'*' * len(settings.DATABASES['default']['PASSWORD'])}")
            return False
            
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def show_current_settings():
    """Show current database settings."""
    try:
        import django
        from django.conf import settings
        
        # Add project to path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, BASE_DIR)
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
        django.setup()
        
        db_config = settings.DATABASES['default']
        print("📋 Current Database Configuration:")
        print(f"   ENGINE: {db_config['ENGINE']}")
        print(f"   NAME: {db_config['NAME']}")
        print(f"   USER: {db_config['USER']}")
        print(f"   PASSWORD: {'*' * len(db_config['PASSWORD'])}")
        print(f"   HOST: {db_config['HOST']}")
        print(f"   PORT: {db_config['PORT']}")
        
    except Exception as e:
        print(f"❌ Could not read settings: {e}")

if __name__ == '__main__':
    print("🔍 Testing PostgreSQL Connection")
    print("=" * 40)
    
    print("\n📋 Current Settings:")
    show_current_settings()
    
    print("\n🧪 Testing Connection...")
    if test_connection():
        print("\n✅ Ready to run migrations!")
        print("   Run: python manage.py migrate")
    else:
        print("\n❌ Please check your PostgreSQL configuration:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Update PASSWORD in settings.py")
        print("   3. Verify database name exists")
