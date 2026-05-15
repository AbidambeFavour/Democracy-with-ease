# Database Setup Guide for SimpleVote

## Option 1: PostgreSQL (Recommended for Production)

### Prerequisites
1. PostgreSQL installed on your system
2. PostgreSQL service running

### Step 1: Install PostgreSQL
**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer and remember your password
- Make sure to install pgAdmin 4

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Create Database
Open pgAdmin or use command line:

**Using pgAdmin:**
1. Connect to PostgreSQL server
2. Right-click on "Databases" → Create → Database
3. Name: `simplevote_db`

**Using Command Line:**
```sql
-- Connect to PostgreSQL as postgres user
psql -U postgres

-- Create database
CREATE DATABASE simplevote_db;

-- Create user (optional)
CREATE USER simplevote_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE simplevote_db TO simplevote_user;

-- Exit
\q
```

### Step 3: Update Django Settings
The settings are already configured in `simplevote/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'simplevote_db',
        'USER': 'postgres',
        'PASSWORD': 'password',  # Update this
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Update the PASSWORD field** with your actual PostgreSQL password.

### Step 4: Install Dependencies
```bash
pip install psycopg2-binary
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

## Option 2: SQLite (Quick Setup for Development)

If you don't want to install PostgreSQL right now, you can use SQLite:

### Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing the Setup

### 1. Start Development Server
```bash
python manage.py runserver
```

### 2. Test Registration
- Go to http://127.0.0.1:8000/accounts/register/
- Fill out the registration form
- Submit to test user creation

### 3. Test Login
- Go to http://127.0.0.1:8000/accounts/login/
- Use the credentials you just created

## Troubleshooting

### Common PostgreSQL Issues:

**"password authentication failed for user 'postgres'"**
- Check your PostgreSQL password
- Update settings.py with correct password

**"connection to server at 'localhost' failed"**
- Make sure PostgreSQL service is running
- Check that port 5432 is available

**"database 'simplevote_db' does not exist"**
- Create the database in PostgreSQL first
- Use pgAdmin or command line to create it

### Django Issues:

**"No changes detected" in makemigrations**
- This is normal if models haven't changed
- Run `python manage.py migrate` anyway

**"ModuleNotFoundError: No module named 'psycopg2'"**
- Install with: `pip install psycopg2-binary`

## Next Steps

1. Choose your database setup (PostgreSQL recommended)
2. Follow the appropriate steps above
3. Test the registration and login forms
4. Create your first poll to test the voting system

## Production Considerations

For production deployment:
- Use PostgreSQL (not SQLite)
- Set `DEBUG = False` in settings.py
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for database credentials
- Set up proper logging
