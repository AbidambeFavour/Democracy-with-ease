# 🚀 Django Voting System - Complete API Documentation for Postman

## 📋 **Overview**
This document provides comprehensive API endpoint documentation for the Django Voting System, designed specifically for Postman testing. The system uses Django's session-based authentication and CSRF protection.

## 🔧 **Base Configuration**
- **Base URL**: `http://localhost:8000` (development)
- **Authentication**: Session-based (Django Auth)
- **CSRF Protection**: Enabled (required for POST/PUT/DELETE)
- **Content-Type**: `application/x-www-form-urlencoded` (forms) or `multipart/form-data` (file uploads)

---

## 🏠 **1. PUBLIC ENDPOINTS (No Authentication Required)**

### 1.1 Landing Page
```http
GET /
```
**Description**: Main landing page showing featured polls and statistics
**Response**: HTML page with poll listings

### 1.2 User Registration
```http
POST /accounts/register/
```
**Description**: Register a new user account
**Content-Type**: `application/x-www-form-urlencoded`

**Request Body**:
```
username=testuser
email=test@example.com
password1=SecurePass123
password2=SecurePass123
first_name=John
last_name=Doe
```

**Response**: 
- Success: Redirect to dashboard
- Error: Registration form with error messages

### 1.3 User Login
```http
POST /accounts/login/
```
**Description**: Authenticate user and create session
**Content-Type**: `application/x-www-form-urlencoded`

**Request Body**:
```
username=testuser
password=SecurePass123
```

**Response**:
- Success: Redirect to dashboard
- Error: Login form with error messages

### 1.4 Poll List
```http
GET /voting/
```
**Description**: Get list of all polls with filtering options
**Query Parameters**:
- `category` (optional): Filter by category slug
- `search` (optional): Search in title, description, tags
- `status` (optional): Filter by status (active, closed, upcoming)

**Examples**:
```
GET /voting/?category=technology
GET /voting/?search=python
GET /voting/?status=active
```

**Response**: HTML page with paginated poll list

### 1.5 Poll Detail
```http
GET /voting/poll/{id}/
```
**Description**: Get detailed information about a specific poll
**URL Parameters**:
- `id`: Poll ID (integer)

**Response**: HTML page with poll details, choices, and voting form

### **1. User Registration**
- **Method:** `POST`
- **URL:** `{{base_url}}/accounts/register/`
- **Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```json
{
    "username": "testuser123",
    "email": "testuser123@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password1": "complexpassword123",
    "password2": "complexpassword123"
}
```

**Expected Response:**
- **Success:** `302 Redirect` to `/accounts/dashboard/`
- **Error:** `200` with form validation errors

**Postman Setup:**
- Type: `POST`
- URL: `http://127.0.0.1:8000/accounts/register/`
- Body: `x-www-form-urlencoded`
- Disable redirects in Postman settings to see response

### **2. User Login**
- **Method:** `POST`
- **URL:** `{{base_url}}/accounts/login/`
- **Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**Expected Response:**
- **Success:** `302 Redirect` to `/accounts/dashboard/`
- **Error:** `200` with error message

### **3. User Logout**
- **Method:** `POST` or `GET`
- **URL:** `{{base_url}}/accounts/logout/`
- **Authentication:** Required (logged in user)

**Expected Response:**
- **Success:** `302 Redirect` to `/accounts/landing/`

---

## 📊 **Poll Management Endpoints**

### **1. List All Polls**
- **Method:** `GET`
- **URL:** `{{base_url}}/voting/`
- **Authentication:** Optional (public polls)

**Query Parameters:**
- `category` (optional): Filter by category slug
- `search` (optional): Search in title/description/tags
- `status` (optional): `active`, `closed`, `upcoming`

**Examples:**
```
GET /voting/?category=politics
GET /voting/?search=election
GET /voting/?status=active
```

**Expected Response:**
```json
{
    "polls": [
        {
            "id": 1,
            "title": "Best Programming Language",
            "description": "Vote for your favorite language",
            "creator": "testuser",
            "created_at": "2024-01-15T10:30:00Z",
            "start_date": "2024-01-15T10:30:00Z",
            "end_date": "2024-01-30T10:30:00Z",
            "is_active": true,
            "is_closed": false,
            "vote_count": 15,
            "category": "Technology",
            "choices": [
                {
                    "id": 1,
                    "text": "Python",
                    "vote_count": 8
                },
                {
                    "id": 2,
                    "text": "JavaScript",
                    "vote_count": 7
                }
            ]
        }
    ],
    "is_paginated": true,
    "page_obj": {
        "has_previous": false,
        "has_next": true,
        "number": 1,
        "num_pages": 3
    }
}
```

### **2. Create New Poll**
- **Method:** `POST`
- **URL:** `{{base_url}}/voting/create/`
- **Authentication:** Required
- **Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```json
{
    "title": "What's your favorite framework?",
    "description": "Choose your preferred web framework",
    "category": "Technology",
    "start_date": "2024-01-15T10:30:00Z",
    "end_date": "2024-01-30T10:30:00Z",
    "choices": [
        {"text": "Django"},
        {"text": "Flask"},
        {"text": "FastAPI"}
    ],
    "tags": ["web", "framework", "backend"]
}
```

**Expected Response:**
- **Success:** `302 Redirect` to new poll detail
- **Error:** `200` with form validation errors

### **3. Get Poll Details**
- **Method:** `GET`
- **URL:** `{{base_url}}/voting/poll/{id}/`
- **Authentication:** Optional (public view)

**Expected Response:**
```json
{
    "poll": {
        "id": 1,
        "title": "Best Programming Language",
        "description": "Vote for your favorite language...",
        "creator": "testuser",
        "created_at": "2024-01-15T10:30:00Z",
        "start_date": "2024-01-15T10:30:00Z",
        "end_date": "2024-01-30T10:30:00Z",
        "is_active": true,
        "is_closed": false,
        "user_voted": false,
        "category": "Technology",
        "tags": ["programming", "language"],
        "choices": [
            {
                "id": 1,
                "text": "Python",
                "vote_count": 8,
                "percentage": 53.3
            },
            {
                "id": 2,
                "text": "JavaScript",
                "vote_count": 7,
                "percentage": 46.7
            }
        ]
    },
    "comments": [
        {
            "id": 1,
            "user": "anotheruser",
            "text": "Great poll!",
            "created_at": "2024-01-16T14:20:00Z"
        }
    ],
    "reactions": {
        "like": 5,
        "love": 2,
        "laugh": 1
    }
}
```

### **4. Vote on Poll**
- **Method:** `POST`
- **URL:** `{{base_url}}/voting/poll/{id}/vote/`
- **Authentication:** Required
- **Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```json
{
    "choice_id": 1
}
```

**Expected Response:**
- **Success:** `302 Redirect` back to poll detail
- **Error:** `200` with error message

### **5. Add Comment**
- **Method:** `POST`
- **URL:** `{{base_url}}/voting/poll/{poll_id}/comment/`
- **Authentication:** Required
- **Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```json
{
    "text": "This is a great poll question!"
}
```

**Expected Response:**
- **Success:** `302 Redirect` back to poll detail
- **Error:** `200` with validation errors

### **6. Toggle Reaction**
- **Method:** `POST`
- **URL:** `{{base_url}}/voting/poll/{poll_id}/react/{reaction_type}/`
- **Authentication:** Required
- **Path Variables:**
  - `poll_id`: Integer poll ID
  - `reaction_type`: String (`like`, `love`, `laugh`)

**Expected Response:**
```json
{
    "status": "success",
    "message": "Reaction added",
    "reactions": {
        "like": 6,
        "love": 2,
        "laugh": 1
    }
}
```

---

## 👤 **User Management Endpoints**

### **1. User Dashboard**
- **Method:** `GET`
- **URL:** `{{base_url}}/accounts/dashboard/`
- **Authentication:** Required

**Expected Response:**
```json
{
    "user": {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "date_joined": "2024-01-10T15:30:00Z",
        "polls_created": 5,
        "votes_cast": 12
    },
    "stats": {
        "total_polls": 5,
        "total_votes_cast": 12,
        "active_polls": 3
    },
    "recent_polls": [
        {
            "id": 1,
            "title": "Sample Poll",
            "vote_count": 8,
            "created_at": "2024-01-15T10:30:00Z"
        }
    ],
    "recent_activity": [
        {
            "description": "User logged in",
            "timestamp": "2024-01-16T09:15:00Z"
        }
    ]
}
```

### **2. User Profile**
- **Method:** `GET`
- **URL:** `{{base_url}}/accounts/profile/{username}/`
- **Authentication:** Optional (public profile)

**Expected Response:**
```json
{
    "profile_user": {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "date_joined": "2024-01-10T15:30:00Z",
        "bio": "Software developer interested in voting systems"
    },
    "polls": [
        {
            "id": 1,
            "title": "Sample Poll",
            "vote_count": 8,
            "created_at": "2024-01-15T10:30:00Z"
        }
    ],
    "votes": [
        {
            "poll_title": "Best Language",
            "choice_text": "Python",
            "voted_at": "2024-01-16T10:30:00Z"
        }
    ]
}
```

### **3. Update Profile**
- **Method:** `POST`
- **URL:** `{{base_url}}/accounts/profile/`
- **Authentication:** Required
- **Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "Updated bio text",
    "location": "New York",
    "website": "https://example.com"
}
```

---

## 🔧 **Admin Endpoints**

### **1. Admin Dashboard**
- **Method:** `GET`
- **URL:** `{{base_url}}/accounts/admin-dashboard/`
- **Authentication:** Required (Staff user)
- **Permission:** `is_staff = True`

**Expected Response:**
```json
{
    "stats": {
        "total_users": 150,
        "active_polls": 25,
        "total_votes": 1250
    },
    "recent_activities": [
        {
            "user": "testuser",
            "description": "User registered",
            "timestamp": "2024-01-16T10:30:00Z"
        }
    ],
    "system_health": {
        "database_status": "healthy",
        "server_uptime": "15 days",
        "memory_usage": "45%"
    }
}
```

### **2. Django Admin Panel**
- **URL:** `{{base_url}}/admin/`
- **Authentication:** Superuser required
- **Features:** Full CRUD operations on all models

---

## 🔄 **AJAX Endpoints**

### **1. Toggle Online Status**
- **Method:** `POST`
- **URL:** `{{base_url}}/accounts/toggle-online/`
- **Authentication:** Required

**Expected Response:**
```json
{
    "status": "success",
    "timestamp": "2024-01-16T10:30:00Z"
}
```

---

## 📝 **Postman Collection Setup**

### **Step 1: Environment Variables**
```json
{
    "base_url": "http://127.0.0.1:8000",
    "csrf_token": "{{extract_from_login_page}}",
    "session_cookie": "{{extract_from_login_response}}"
}
```

### **Step 2: Authentication Flow**
1. **GET** `/accounts/login/` - Extract CSRF token from HTML
2. **POST** `/accounts/login/` - Send credentials with CSRF
3. **Extract** session cookie from response
4. **Use** session cookie for subsequent requests

### **Step 3: Common Headers**
```
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid={{session_cookie}}
X-CSRFToken: {{csrf_token}}
Referer: {{base_url}}
```

---

## ⚠️ **Important Notes**

### **CSRF Protection**
- All POST requests require valid CSRF token
- Extract from form inputs or meta tags
- Include in `X-CSRFToken` header

### **Session Management**
- Django uses session-based authentication
- Cookies are automatically handled by browser
- Session expires on logout

### **Error Handling**
- **200 OK:** Form validation errors in HTML
- **302 Found:** Success (redirect)
- **404 Not Found:** Resource doesn't exist
- **403 Forbidden:** Permission denied
- **500 Server Error:** Internal error

### **Rate Limiting**
- No explicit rate limiting configured
- Consider implementing for production

---

## 🧪 **Testing Workflows**

### **Workflow 1: Complete User Journey**
1. Register new user
2. Login with credentials
3. View dashboard
4. Create new poll
5. Vote on poll
6. Add comment
7. Logout

### **Workflow 2: Admin Operations**
1. Login as admin user
2. View admin dashboard
3. Access Django admin panel
4. Manage users and polls

### **Workflow 3: Public Access**
1. View poll list (no auth required)
2. View poll details
3. Search polls
4. Filter by category

---

## 📊 **Response Formats**

### **Success Responses**
- **302 Redirect:** Operation successful
- **200 OK:** Data returned (GET requests)

### **Error Responses**
- **200 OK with HTML:** Form errors displayed
- **400 Bad Request:** Invalid data
- **401 Unauthorized:** Not logged in
- **403 Forbidden:** No permission
- **404 Not Found:** Resource missing
- **500 Server Error:** Internal error

---

## 🚀 **Ready for Testing**

Import this collection into Postman and start testing all endpoints. The system is fully functional with PostgreSQL database integration!
