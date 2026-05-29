# Render PostgreSQL Database Setup Guide

This guide will help you set up PostgreSQL on Render and ensure your Django voting system stores data correctly.

## Problem: Data Not Persisting

If polls and users are not storing in the database, it's likely because:
1. Your app is using SQLite instead of PostgreSQL
2. PostgreSQL is not properly configured on Render
3. Database migrations haven't been run on the production database

## Solution: Set Up PostgreSQL on Render

### Step 1: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure the database:
   - **Name**: `democracy-voting-db` (or your preferred name)
   - **Database**: `democracy_voting` (or your preferred name)
   - **User**: `democracy_admin` (or your preferred name)
   - **Region**: Choose the same region as your web service
   - **Plan**: Free tier is fine for development
4. Click **"Create Database"**

### Step 2: Get Database Connection URL

1. After creation, click on your PostgreSQL database
2. Scroll down to the **"Connections"** section
3. Copy the **"Internal Database URL"**
   - It looks like: `postgres://democracy_admin:password@host:5432/democracy_voting`

### Step 3: Add DATABASE_URL to Your Web Service

1. Go to your web service (democracy-with-ease)
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Add a new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: (paste the Internal Database URL from Step 2)
5. Click **"Save Changes"**

### Step 4: Run Database Migrations

Your Django settings are already configured to automatically use PostgreSQL when `DATABASE_URL` is set. However, you need to run migrations to create the tables.

#### Option A: Automatic Migration (Recommended)

Render can automatically run migrations during deployment. Add this to your `package.json` or use Render's build command:

```json
{
  "scripts": {
    "build": "python manage.py collectstatic --noinput && python manage.py migrate --noinput"
  }
}
```

#### Option B: Manual Migration via Render Shell

1. Go to your web service on Render
2. Click **"Shell"** tab
3. Run the following commands:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # Optional: Create admin user
   ```

#### Option C: Manual Migration via SSH

1. Enable SSH access in Render dashboard
2. SSH into your Render service
3. Run migration commands as above

### Step 5: Verify Database Connection

1. Check your Render service logs
2. Look for successful migration messages
3. Try creating a test poll or user
4. Verify the data persists after page refresh

## Troubleshooting

### Issue: "relation does not exist" errors

**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Issue: "could not connect to server" errors

**Solution**: Check DATABASE_URL environment variable:
- Ensure it's set correctly in Render dashboard
- Verify the database is running
- Check that the database and web service are in the same region

### Issue: Data still not persisting

**Solution**: Verify PostgreSQL is being used:
1. Add this to your views temporarily to check:
   ```python
   from django.db import connection
   print(f"Database engine: {connection.settings_dict['ENGINE']}")
   ```
2. If it shows SQLite, DATABASE_URL is not set correctly

### Issue: Migration errors

**Solution**: Reset migrations:
```bash
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb
```

## Admin Delete Functionality

Your system now includes admin delete functionality:

### Delete Polls
- Go to **Admin Dashboard** → **Manage Polls**
- Click **"Delete"** button next to any poll
- Confirm deletion

### Delete Users
- Go to **Admin Dashboard** → **Manage Users**
- Click **"Delete"** button next to any user (except yourself)
- Confirm deletion

## Database Tables Created

When migrations run successfully, these tables will be created:

### Accounts App
- `accounts_user` (Custom user model)
- `accounts_userprofile` (User preferences)
- `accounts_useractivity` (User activity tracking)

### Voting App
- `voting_category` (Poll categories)
- `voting_poll` (Voting polls)
- `voting_choice` (Poll choices)
- `voting_vote` (User votes)
- `voting_pollcomment` (Poll comments)
- `voting_pollreaction` (Poll reactions)
- `voting_usernotification` (User notifications)

### Django Built-in Tables
- `django_migrations` (Migration tracking)
- `django_admin_log` (Admin actions)
- `django_content_type` (Content types)
- `django_auth_permission` (Permissions)
- `django_session` (Sessions)

## Verification Checklist

- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL environment variable set
- [ ] Database migrations run successfully
- [ ] Can create polls and they persist
- [ ] Can create users and they persist
- [ ] Admin can delete polls
- [ ] Admin can delete users
- [ ] Data survives page refreshes
- [ ] Data survives service restarts

## Next Steps

1. Complete the PostgreSQL setup above
2. Run migrations to create all tables
3. Test creating a poll and verify it persists
4. Test admin delete functionality
5. Monitor Render logs for any database errors

## Support

If you encounter issues:
1. Check Render service logs
2. Verify DATABASE_URL is correct
3. Ensure PostgreSQL database is running
4. Check that migrations completed successfully
5. Review Django settings for database configuration
