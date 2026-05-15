# Forms Testing Guide for SimpleVote

## 🚀 Server Status
✅ **Development server is running at:** http://127.0.0.1:8000/

## 📋 Test Users Created
- **Username:** `testuser` | **Password:** `password123`
- **Username:** `voter` | **Password:** `password123`
- **Admin:** `admin` | **Password:** (check existing)

## 🧪 Testing the Forms

### 1. Registration Form Test
**URL:** http://127.0.0.1:8000/accounts/register/

**Steps:**
1. Open the registration page
2. Fill in the form with new user details:
   - Username: `newuser`
   - Email: `newuser@example.com`
   - First Name: `New`
   - Last Name: `User`
   - Password: `newpassword123`
   - Confirm Password: `newpassword123`
3. Click "Create Account"
4. **Expected:** Should redirect to login or dashboard

### 2. Login Form Test
**URL:** http://127.0.0.1:8000/accounts/login/

**Steps:**
1. Open the login page
2. Use existing test user:
   - Username: `testuser`
   - Password: `password123`
3. Click "Sign In"
4. **Expected:** Should redirect to dashboard or landing page

### 3. Form Validation Tests

#### Registration Form Validation:
- **Empty fields:** Should show validation errors
- **Mismatched passwords:** Should show "Passwords don't match"
- **Invalid email:** Should show "Enter a valid email address"
- **Duplicate username/email:** Should show "User with this username/email already exists"

#### Login Form Validation:
- **Wrong credentials:** Should show "Please enter a correct username/email and password"
- **Empty fields:** Should show validation errors

## 🔧 Database Status

### Current Setup: SQLite (for immediate testing)
- **Database file:** `db.sqlite3`
- **Status:** ✅ Working
- **Tables:** ✅ Created via migrations

### PostgreSQL Setup (for production)
- **Status:** ⚙️ Configured but not active
- **Switch to PostgreSQL:** Uncomment PostgreSQL settings in `simplevote/settings.py`
- **See:** `DATABASE_SETUP.md` for complete PostgreSQL guide

## 📊 Database Tables Created

### Accounts App:
- `accounts_user` (Custom user model)
- `accounts_userprofile` (User preferences)
- `accounts_useractivity` (Activity tracking)

### Voting App:
- `voting_category` (Poll categories)
- `voting_poll` (Polls)
- `voting_choice` (Poll choices)
- `voting_vote` (Votes)
- `voting_pollcomment` (Comments)
- `voting_pollreaction` (Reactions)

### Django Built-in:
- `auth_user` (Django auth)
- `django_migrations` (Migration tracking)
- `django_session` (Sessions)

## 🧪 Additional Testing

### Test User Registration via Django Admin:
1. Go to http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Navigate to "Users" section
4. Add new users to test registration flow

### Test Form Field Types:
- **Text inputs:** Username, names
- **Email input:** Email validation
- **Password inputs:** Password confirmation
- **File input:** Avatar upload (if enabled)

## 🔍 Debugging Tips

### If Forms Don't Work:
1. **Check browser console** for JavaScript errors
2. **Check Django logs** in terminal
3. **Verify CSRF token** is present
4. **Check form action** URL is correct

### Common Issues:
- **CSRF Token Missing:** Django forms include CSRF protection automatically
- **Form Not Valid:** Check form validation errors
- **Database Error:** Ensure migrations are applied

## 📱 Responsive Testing

### Test on Different Screen Sizes:
- **Desktop:** Full browser window
- **Tablet:** ~768px width
- **Mobile:** ~375px width

### Form Elements to Check:
- Input field sizing
- Button spacing
- Error message display
- Navigation links

## 🚀 Next Steps

1. **Test all forms** with the provided test users
2. **Verify database connections** are working
3. **Set up PostgreSQL** for production (optional)
4. **Test voting functionality** once users are created
5. **Test admin panel** for content management

## 📞 Support

If forms don't work:
1. Check the terminal output for errors
2. Verify the server is running
3. Try refreshing the page
4. Check `DATABASE_SETUP.md` for database issues

---

**Server Running:** ✅ http://127.0.0.1:8000/
**Database:** ✅ SQLite (Ready for testing)
**Test Users:** ✅ Created
