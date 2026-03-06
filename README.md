# SimpleVote - Democratic Voting System

A clean, simple, and elegant Django-based voting system designed for small groups like classrooms, meetings, and clubs.

## Features

- **Clean & Responsive UI**: Built with Bootstrap 5 for a modern, mobile-friendly interface
- **Poll Creation**: Easy-to-use form for creating polls with multiple choices
- **Time-Based Voting**: Set start and end times for automatic poll activation/closure
- **One Vote Per Person**: Session-based voting enforcement (no registration required)
- **Anonymous Voting**: Results are hidden until polls close
- **Visual Results**: Beautiful charts and progress bars showing final results
- **Admin Interface**: Full Django admin integration for managing polls

## Technical Stack

- **Backend**: Django 4.2+ (LTS)
- **Frontend**: Django templates with Bootstrap 5
- **Database**: SQLite (default, easily configurable)
- **Charts**: Chart.js for result visualization
- **Python**: 3.10+

## Project Structure

```
simplevote/
├── manage.py
├── requirements.txt
├── simplevote/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── voting/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── templates/
    ├── base.html
    └── voting/
        ├── poll_list.html
        ├── poll_detail.html
        └── create_poll.html
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

Visit `http://127.0.0.1:8000/admin/` to access the admin interface.

## Usage

### Creating Polls

1. Click "Create New Poll" on the homepage
2. Fill in the poll title and optional description
3. Set start and end dates/times
4. Add at least two choices for the poll
5. Click "Create Poll"

### Voting

1. Browse active polls on the homepage
2. Click "Vote" on any active poll
3. Select your choice and submit
4. You'll see a confirmation message (results are hidden until poll closes)

### Viewing Results

- Results are automatically displayed when a poll closes
- View closed polls to see detailed results with charts and percentages
- Admin users can view all poll statistics in the admin interface

## Key Features Explained

### Session-Based Voting

The system uses Django sessions to ensure one vote per person per poll:
- Each browser session gets a unique identifier
- Votes are tracked by session key and poll ID
- No user registration required (perfect for small, trusted groups)

### Anonymous Voting

- While polls are active, no vote counts or results are shown
- This prevents bias and ensures honest voting
- Results are revealed automatically when polls close

### Time-Based Control

- Polls automatically activate at their start time
- Polls automatically close at their end time
- Clear status indicators (Upcoming, Active, Closed)

## Admin Features

The Django admin interface provides:

- **Poll Management**: Create, edit, and delete polls
- **Choice Management**: Add/remove choices from polls
- **Vote Tracking**: View all votes with timestamps and session IDs
- **Statistics**: See vote counts and percentages for each choice
- **Bulk Operations**: Manage multiple polls efficiently

## Security Notes

- Uses Django's built-in CSRF protection
- Session-based voting prevents duplicate votes
- Admin interface protected by Django authentication
- SQL injection protection through Django ORM

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS` appropriately
3. Set up a production database (PostgreSQL recommended)
4. Configure static files serving
5. Set up proper logging
6. Use HTTPS for secure connections

## Customization

The system is easily customizable:

- **Styling**: Modify Bootstrap classes or add custom CSS
- **Features**: Extend models and views for additional functionality
- **Authentication**: Add user registration if needed
- **Notifications**: Add email notifications for poll events

## License

This project is open source and available under the MIT License.
