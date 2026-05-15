#!/usr/bin/env python
"""
Find the correct PostgreSQL password by testing common passwords.
"""

import psycopg2

def test_passwords():
    """Test common PostgreSQL passwords."""
    
    # Common passwords to try
    passwords = [
        'postgres',
        'password', 
        'admin',
        '123456',
        'root',
        '1234',
        '',  # empty password
        'p@ssword',
        'PostgreSQL',
        'postgres123',
        'password123'
    ]
    
    print("🔍 Testing common PostgreSQL passwords...")
    print("=" * 50)
    
    for password in passwords:
        try:
            conn = psycopg2.connect(
                dbname='simplevote_db',
                user='postgres',
                password=password,
                host='localhost',
                port='5432'
            )
            print(f"✅ SUCCESS! Password found: '{password}'")
            print(f"📝 Update your settings.py PASSWORD to: '{password}'")
            conn.close()
            return password
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                print(f"❌ '{password}' - Incorrect")
            elif "does not exist" in str(e):
                print(f"❌ Database 'simplevote_db' does not exist")
                print("📋 Create database first: CREATE DATABASE simplevote_db;")
                return None
            else:
                print(f"❌ '{password}' - Error: {e}")
    
    print("\n❌ No working password found!")
    print("\n🔧 Solutions:")
    print("1. Check your PostgreSQL installation")
    print("2. Try connecting with pgAdmin to find the correct password")
    print("3. Reset the postgres password:")
    print("   - Stop PostgreSQL service")
    print("   - Run: ALTER USER postgres PASSWORD 'new_password';")
    print("4. Reinstall PostgreSQL if needed")
    
    return None

if __name__ == '__main__':
    found_password = test_passwords()
    
    if found_password:
        print(f"\n🎉 Password found: '{found_password}'")
        print("Update your settings.py and run migrations!")
    else:
        print("\n❌ Please check your PostgreSQL setup")
