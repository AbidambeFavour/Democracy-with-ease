# PostgreSQL Troubleshooting Guide

## Current Issue
Password authentication failed for user 'Favour'

## Possible Solutions

### 1. Check PostgreSQL User Exists
Connect to PostgreSQL and verify the user exists:

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Check if user 'Favour' exists
\du

-- If user doesn't exist, create it:
CREATE USER Favour WITH PASSWORD 'p@ssword';

-- Grant necessary privileges
GRANT ALL PRIVILEGES ON DATABASE simplevote_db TO Favour;
```

### 2. Alternative: Use postgres user
If the 'Favour' user doesn't have proper privileges, try using the default postgres user:

Update settings.py:
```python
'USER': 'postgres',
'PASSWORD': 'your_postgres_password',  # Try 'postgres', 'password', etc.
```

### 3. Check pg_hba.conf Configuration
PostgreSQL might not allow password authentication for your user. Check:
- File location: `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`
- Look for lines like: `host    all             all             127.0.0.1/32            md5`

### 4. Test Connection Directly
Test with psql command:
```bash
psql -h localhost -U Favour -d simplevote_db -W
```

### 5. Common PostgreSQL Default Passwords
Try these as the postgres user password:
- `postgres`
- `password`
- `admin`
- `123456`
- (leave empty)

## Quick Fix Options

### Option A: Use postgres user (recommended)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'simplevote_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',  # Try this first
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Option B: Create proper user
1. Connect to PostgreSQL as postgres user
2. Run: `CREATE USER Favour WITH PASSWORD 'p@ssword' CREATEDB;`
3. Run: `GRANT ALL PRIVILEGES ON DATABASE simplevote_db TO Favour;`

## Next Steps
1. Try Option A first (postgres user)
2. If that works, run migrations
3. If not, check PostgreSQL installation
4. Verify database exists: `\l` in psql
