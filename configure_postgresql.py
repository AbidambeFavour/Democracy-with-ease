#!/usr/bin/env python
"""
PostgreSQL configuration helper for SimpleVote.
"""

import os

def create_env_file():
    """Create .env file for database credentials."""
    env_content = """# PostgreSQL Database Configuration
# Update these values with your actual PostgreSQL credentials

DB_NAME=simplevote_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password_here
DB_HOST=localhost
DB_PORT=5432

# Django Secret Key (keep this secret!)
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    print("📝 Please update DB_PASSWORD with your actual PostgreSQL password")

def update_settings_with_env():
    """Show how to update settings.py to use environment variables."""
    settings_update = """
# Add this to the top of settings.py:
from dotenv import load_dotenv
load_dotenv()

# Replace DATABASES section with:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'simplevote_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
"""
    
    print("📋 To use environment variables, update settings.py with:")
    print(settings_update)

def check_connection():
    """Test PostgreSQL connection with different credentials."""
    import psycopg2
    
    # Common default passwords to try
    test_passwords = ['password', 'postgres', 'admin', '123456', '', 'root']
    
    print("🔍 Testing PostgreSQL connection...")
    
    for password in test_passwords:
        try:
            conn = psycopg2.connect(
                dbname='simplevote_db',
                user='postgres',
                password=password,
                host='localhost',
                port='5432'
            )
            print(f"✅ Connected successfully with password: '{password}'")
            print(f"📝 Update your settings.py PASSWORD to: '{password}'")
            conn.close()
            return password
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                continue
            else:
                print(f"❌ Error with password '{password}': {e}")
    
    print("❌ Could not connect with any common password")
    print("📋 Please check your PostgreSQL installation and credentials")
    return None

if __name__ == '__main__':
    print("🔧 PostgreSQL Configuration Helper")
    print("=" * 40)
    
    print("\n1. Creating .env file...")
    create_env_file()
    
    print("\n2. Checking PostgreSQL connection...")
    try:
        import psycopg2
        password = check_connection()
        if password:
            print(f"\n✅ Use this password in settings.py: PASSWORD = '{password}'")
    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
    
    print("\n3. Environment variables setup...")
    update_settings_with_env()
    
    print("\n📋 Next steps:")
    print("1. Update DB_PASSWORD in .env file")
    print("2. Or update PASSWORD directly in settings.py")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py createsuperuser")
