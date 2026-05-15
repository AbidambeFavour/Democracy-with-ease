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

---

## 🔐 **2. AUTHENTICATED ENDPOINTS (Login Required)**

### 2.1 User Dashboard
```http
GET /accounts/dashboard/
```
**Description**: User's personal dashboard with statistics and activity
**Authentication**: Required (session)
**Response**: HTML dashboard with user's polls, votes, and statistics

### 2.2 User Logout
```http
POST /accounts/logout/
```
**Description**: Logout user and destroy session
**Authentication**: Required (session)
**Response**: Redirect to landing page

### 2.3 Create Poll
```http
GET /voting/create/
POST /voting/create/
```
**Description**: Create a new poll
**Authentication**: Required (session)

**POST Request Body** (multipart/form-data):
```
title=Best Programming Language
description=Vote for your favorite programming language
category=1
tags=programming,technology,survey
start_date=2024-01-01
start_time=10:00
end_date=2024-01-31
end_time=23:59
is_public=on
allow_multiple_votes=off
max_votes_per_user=1
show_results_immediately=off
choice_1=Python
choice_2=JavaScript
choice_3=Java
choice_4=C++
```

**Response**:
- Success: Redirect to poll detail page
- Error: Creation form with error messages

### 2.4 Vote in Poll
```http
POST /voting/poll/{id}/
```
**Description**: Cast a vote in a poll
**Authentication**: Required (session)
**URL Parameters**:
- `id`: Poll ID (integer)

**Request Body**:
```
choice=5
```

**Response**: Redirect to poll detail page with success/error message

### 2.5 Add Comment to Poll
```http
POST /voting/poll/{poll_id}/comment/
```
**Description**: Add a comment to a poll
**Authentication**: Required (session)
**URL Parameters**:
- `poll_id`: Poll ID (integer)

**Request Body**:
```
content=This is a great poll! I voted for Python.
```

**Response**: Redirect to poll detail page

### 2.6 Toggle Poll Reaction
```http
POST /voting/poll/{poll_id}/react/{reaction_type}/
```
**Description**: Add or remove reaction from a poll
**Authentication**: Required (session)
**URL Parameters**:
- `poll_id`: Poll ID (integer)
- `reaction_type`: One of: like, dislike, love, laugh, wow

**Examples**:
```
POST /voting/poll/5/react/like/
POST /voting/poll/5/react/love/
```

**Response**: Redirect to poll detail page

### 2.7 Update User Profile
```http
GET /accounts/profile/
POST /accounts/profile/
```
**Description**: Update user profile information
**Authentication**: Required (session)

**POST Request Body** (multipart/form-data):
```
first_name=John
last_name=Doe
email=john.doe@example.com
bio=Software developer passionate about Python
date_of_birth=1990-01-01
location=San Francisco
website=https://johndoe.dev
phone_number=+1234567890
email_notifications=on
push_notifications=off
public_profile=on
show_email=off
show_real_name=on
theme=light
language=en
timezone=UTC
```

**Response**: Profile update page with success/error messages

### 2.8 View User Profile
```http
GET /accounts/profile/{username}/
```
**Description**: View another user's public profile
**Authentication**: Optional (session)
**URL Parameters**:
- `username`: Username string

**Response**: HTML profile page with user's polls and activity

### 2.9 Admin Dashboard
```http
GET /accounts/admin-dashboard/
```
**Description**: Admin dashboard with system statistics
**Authentication**: Required (session + staff status)
**Response**: HTML admin dashboard with system statistics

### 2.10 Toggle Online Status (AJAX)
```http
POST /accounts/toggle-online/
```
**Description**: Update user's last seen timestamp
**Authentication**: Required (session)
**Content-Type**: `application/x-www-form-urlencoded`
**Response**: JSON response
```json
{"status": "success"}
```

---

## 🔍 **3. SPECIAL ENDPOINTS & FEATURES**

### 3.1 Password Reset Endpoints
```http
GET /accounts/password-reset/
POST /accounts/password-reset/
GET /accounts/password-reset/done/
GET /accounts/password-reset-confirm/{uidb64}/{token}/
POST /accounts/password-reset-confirm/{uidb64}/{token}/
GET /accounts/password-reset-complete/
```
**Description**: Django's built-in password reset functionality
**Authentication**: Not required (email-based)

### 3.2 Admin Panel
```http
GET /admin/
```
**Description**: Django admin interface for database management
**Authentication**: Required (admin user)

---

## 🧪 **4. TESTING IN POSTMAN - STEP BY STEP GUIDE**

### 4.1 Initial Setup
1. **Create New Collection**: "Django Voting System API"
2. **Set Collection Variables**:
   - `baseUrl`: `http://localhost:8000`
   - `username`: `testuser`
   - `password`: `SecurePass123`

### 4.2 Authentication Flow Testing

#### Step 1: Register New User
```http
POST {{baseUrl}}/accounts/register/
```
**Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Body** (x-www-form-urlencoded):
```
username={{username}}
email=test@example.com
password1={{password}}
password2={{password}}
first_name=Test
last_name=User
```

**Tests Script**:
```javascript
pm.test("Registration successful", function() {
    pm.response.to.have.status(302); // Redirect on success
});
```

#### Step 2: Login User
```http
POST {{baseUrl}}/accounts/login/
```
**Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Body** (x-www-form-urlencoded):
```
username={{username}}
password={{password}}
csrfmiddlewaretoken={{csrf_token}}
```

**Tests Script**:
```javascript
pm.test("Login successful", function() {
    pm.response.to.have.status(302);
});

// Extract session cookie
const cookies = pm.response.headers.get('Set-Cookie');
if (cookies) {
    pm.collectionVariables.set('session_cookie', cookies);
}
```

### 4.3 CSRF Token Handling
Since Django uses CSRF protection, you need to handle CSRF tokens:

#### Get CSRF Token First
```http
GET {{baseUrl}}/accounts/login/
```

**Tests Script**:
```javascript
// Extract CSRF token from HTML
const html = pm.response.text();
const csrfMatch = html.match(/name='csrfmiddlewaretoken' value='([^']+)'/);
if (csrfMatch) {
    pm.collectionVariables.set('csrf_token', csrfMatch[1]);
}
```

#### Use CSRF Token in POST Requests
Include in your POST requests:
```
csrfmiddlewaretoken={{csrf_token}}
```

### 4.4 Testing Poll Creation

#### Step 1: Get Categories (for form)
```http
GET {{baseUrl}}/voting/create/
```

#### Step 2: Create Poll
```http
POST {{baseUrl}}/voting/create/
```
**Headers**:
```
Content-Type: multipart/form-data
Cookie: {{session_cookie}}
```

**Body** (form-data):
```
title: Test Poll from Postman
description: This is a test poll created via Postman API
category: 1
tags: test,postman,api
start_date: 2024-01-01
start_time: 10:00
end_date: 2024-12-31
end_time: 23:59
is_public: true
allow_multiple_votes: false
max_votes_per_user: 1
show_results_immediately: true
choice_1: Option A
choice_2: Option B
choice_3: Option C
csrfmiddlewaretoken: {{csrf_token}}
```

### 4.5 Testing Voting

#### Step 1: Get Poll Details
```http
GET {{baseUrl}}/voting/poll/1/
```

#### Step 2: Cast Vote
```http
POST {{baseUrl}}/voting/poll/1/
```
**Headers**:
```
Content-Type: application/x-www-form-urlencoded
Cookie: {{session_cookie}}
```

**Body**:
```
choice: 1
csrfmiddlewaretoken: {{csrf_token}}
```

---

## 📊 **5. RESPONSE CODES & ERROR HANDLING**

### Success Codes:
- `200 OK`: Successful GET request
- `302 Found`: Successful POST/PUT/DELETE (redirect)
- `201 Created`: Resource created successfully

### Error Codes:
- `400 Bad Request`: Invalid form data
- `403 Forbidden`: CSRF token missing/invalid or permission denied
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: HTTP method not supported

### Common Error Responses:
```json
{
    "error": "Invalid form data",
    "errors": {
        "title": ["This field is required."],
        "email": ["Enter a valid email address."]
    }
}
```

---

## 🔧 **6. POSTMAN COLLECTION TIPS**

### 6.1 Collection Variables
Set these at collection level:
- `baseUrl`: `http://localhost:8000`
- `csrf_token`: Extracted from forms
- `session_cookie`: Extracted after login

### 6.2 Pre-request Script
Add this to collection or folder level to handle CSRF:
```javascript
// Automatically get CSRF token for POST requests
if (pm.request.method === 'POST' || pm.request.method === 'PUT' || pm.request.method === 'DELETE') {
    if (!pm.collectionVariables.get('csrf_token')) {
        pm.sendRequest({
            url: pm.collectionVariables.get('baseUrl') + '/accounts/login/',
            method: 'GET'
        }, function (err, res) {
            if (!err) {
                const html = res.text();
                const csrfMatch = html.match(/name='csrfmiddlewaretoken' value='([^']+)'/);
                if (csrfMatch) {
                    pm.collectionVariables.set('csrf_token', csrfMatch[1]);
                }
            }
        });
    }
}
```

### 6.3 Test Scripts
Add these for validation:
```javascript
// Basic response validation
pm.test("Response time is acceptable", function() {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});

pm.test("Status code is success", function() {
    pm.expect(pm.response.code).to.be.oneOf([200, 302]);
});

// Check for Django error pages
pm.test("No Django error page", function() {
    const text = pm.response.text();
    pm.expect(text).to.not.include("Page not found (404)");
    pm.expect(text).to.not.include("Server Error (500)");
});
```

---

## 🚨 **7. IMPORTANT TESTING NOTES**

### 7.1 Session Management
- Django uses session-based authentication
- Maintain cookies between requests
- Use Postman's cookie jar or manual cookie handling

### 7.2 CSRF Protection
- All POST/PUT/DELETE requests need CSRF token
- Extract token from GET requests first
- Include token in form data

### 7.3 File Uploads
- Use `multipart/form-data` for file uploads
- Use `application/x-www-form-urlencoded` for regular forms

### 7.4 Testing Workflow
1. **Register** → **Login** → **Get CSRF Token** → **Test APIs**
2. Maintain session throughout testing
3. Handle redirects appropriately
4. Check for Django messages in responses

---

## 📝 **8. SAMPLE TEST SEQUENCE**

### Complete User Journey Test:
1. `POST /accounts/register/` - Register user
2. `POST /accounts/login/` - Login user
3. `GET /accounts/dashboard/` - Check dashboard
4. `GET /voting/create/` - Get creation form
5. `POST /voting/create/` - Create poll
6. `GET /voting/poll/1/` - View poll
7. `POST /voting/poll/1/` - Vote in poll
8. `POST /voting/poll/1/comment/` - Add comment
9. `POST /voting/poll/1/react/like/` - Add reaction
10. `POST /accounts/logout/` - Logout

This comprehensive documentation should help you test all aspects of the Django Voting System API using Postman effectively!
