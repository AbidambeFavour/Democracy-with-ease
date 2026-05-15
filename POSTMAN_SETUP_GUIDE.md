# 🚀 **Complete Postman Setup Guide for SimpleVote**

## 📋 **Quick Start Instructions**

### **Step 1: Import Collection into Postman**

1. **Open Postman Desktop App**
2. **Click Import** (top left button)
3. **Select File** tab
4. **Choose:** `SimpleVote_Postman_Collection_Fixed.json`
5. **Click Import**

### **Step 2: Configure Environment**

1. **Click Environments** (left sidebar)
2. **Click Add** to create new environment
3. **Environment Name:** `SimpleVote Dev`
4. **Add Variables:**
   - **Variable:** `base_url` | **Value:** `http://127.0.0.1:8000`
   - **Variable:** `csrf_token` | **Value:** `{{extract_from_login_page}}`
   - **Variable:** `session_cookie` | **Value:** `{{extract_from_login_response}}`

### **Step 3: Set Active Environment**

1. **Select:** `SimpleVote Dev` from environment dropdown
2. **All requests** will now use the base URL automatically

---

## 🔐 **Authentication Flow in Postman**

### **Important Notes:**
- This is a **Django web app**, not a REST API
- Uses **session-based authentication** (not JWT tokens)
- **CSRF protection** enabled on all POST requests
- **302 Redirects** indicate success

### **Authentication Workflow:**

#### **1. Get CSRF Token First**
```
GET /accounts/login/
```
- **Purpose:** Extract CSRF token from the login form
- **Response:** HTML page with CSRF token
- **Extraction:** Look for `csrfmiddlewaretoken` in the HTML

#### **2. Login with Credentials**
```
POST /accounts/login/
Content-Type: application/x-www-form-urlencoded

username: testuser
password: password123
csrfmiddlewaretoken: {{extracted_csrf_token}}
```

#### **3. Extract Session Cookie**
- **From:** Login response headers
- **Look for:** `Set-Cookie: sessionid=...`
- **Save:** For subsequent requests

---

## 📊 **Available Endpoints**

### **Authentication Endpoints**

| Method | Endpoint | Description | Auth Required |
|---------|----------|-------------|---------------|
| GET | `/accounts/landing/` | Landing page | No |
| POST | `/accounts/register/` | User registration | No |
| POST | `/accounts/login/` | User login | No |
| POST | `/accounts/logout/` | User logout | Yes |

### **Poll Management Endpoints**

| Method | Endpoint | Description | Auth Required |
|---------|----------|-------------|---------------|
| GET | `/voting/` | List all polls | No |
| POST | `/voting/create/` | Create new poll | Yes |
| GET | `/voting/poll/{id}/` | Get poll details | No |
| POST | `/voting/poll/{id}/vote/` | Vote on poll | Yes |
| POST | `/voting/poll/{id}/comment/` | Add comment | Yes |
| POST | `/voting/poll/{id}/react/{type}/` | Toggle reaction | Yes |

### **User Management Endpoints**

| Method | Endpoint | Description | Auth Required |
|---------|----------|-------------|---------------|
| GET | `/accounts/dashboard/` | User dashboard | Yes |
| GET | `/accounts/profile/{username}/` | User profile | No |
| POST | `/accounts/profile/` | Update profile | Yes |
| GET | `/accounts/admin-dashboard/` | Admin dashboard | Staff |
| GET | `/admin/` | Django admin | Superuser |

---

## 🔧 **Request Examples**

### **1. User Registration**
```http
POST /accounts/register/
Content-Type: application/x-www-form-urlencoded

username=newuser&email=newuser%40example.com&first_name=New&last_name=User&password1=pass123&password2=pass123
```

### **2. User Login**
```http
POST /accounts/login/
Content-Type: application/x-www-form-urlencoded

username=testuser&password=password123&csrfmiddlewaretoken={{csrf_token}}
```

### **3. List Polls with Filters**
```http
GET /voting/?category=technology&search=python&status=active
```

### **4. Create New Poll**
```http
POST /voting/create/
Content-Type: application/x-www-form-urlencoded

title=Best%20Python%20Framework&description=Choose%20your%20favorite&category=Technology&choices=Django&choices=Flask&choices=FastAPI
```

### **5. Vote on Poll**
```http
POST /voting/poll/1/vote/
Content-Type: application/x-www-form-urlencoded

choice_id=1&csrfmiddlewaretoken={{csrf_token}}
```

---

## 🧪 **Testing Workflows**

### **Workflow 1: Complete User Journey**
1. **Register User:** `POST /accounts/register/`
2. **Login User:** `POST /accounts/login/`
3. **View Dashboard:** `GET /accounts/dashboard/`
4. **Create Poll:** `POST /voting/create/`
5. **Vote on Poll:** `POST /voting/poll/1/vote/`
6. **Logout:** `POST /accounts/logout/`

### **Workflow 2: Anonymous Browsing**
1. **View Landing:** `GET /accounts/landing/`
2. **Browse Polls:** `GET /voting/`
3. **Search Polls:** `GET /voting/?search=python`
4. **View Poll Details:** `GET /voting/poll/1/`

### **Workflow 3: Admin Operations**
1. **Login as Admin:** Use staff credentials
2. **View Admin Dashboard:** `GET /accounts/admin-dashboard/`
3. **Access Django Admin:** `GET /admin/`
4. **Manage Users:** Through Django admin interface

---

## ⚠️ **Important Considerations**

### **CSRF Protection**
- **All POST requests** require valid CSRF token
- **Extract from:** Login page HTML or previous response
- **Include in:** Request headers or form data

### **Session Management**
- **Automatic:** Browser handles cookies
- **Manual:** Extract and include in Postman requests
- **Expires:** On logout or timeout

### **Response Handling**
- **302 Redirects:** Success (check Location header)
- **200 OK:** Form errors or data returned
- **404 Not Found:** Resource doesn't exist
- **403 Forbidden:** Permission denied
- **401 Unauthorized:** Not logged in

### **Content Types**
- **Forms:** `application/x-www-form-urlencoded`
- **API-like:** `application/json` (if implemented)
- **File Upload:** `multipart/form-data` (if implemented)

---

## 🔍 **Debugging Tips**

### **Check Response Headers**
```javascript
// In Postman Tests
pm.test("Status code is 200", function() {
    pm.response.to.have.status(200);
});

// Check for redirect
pm.test("Redirect location header", function() {
    pm.response.to.have.header("Location");
});

// Extract session cookie
pm.test("Session cookie set", function() {
    pm.response.to.have.header("Set-Cookie");
});
```

### **Extract CSRF Token**
```javascript
// Extract CSRF from login page HTML
var $ = cheerio.load(pm.response.text());
var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
pm.environment.set("csrf_token", csrfToken);
```

### **Handle Redirects**
- **Disable:** "Automatically follow redirects" in Postman settings
- **Manual:** Check Location header for redirect URL
- **Expected:** 302 status with Location header

---

## 📱 **Mobile Testing**

### **Postman Mobile App**
1. **Download:** Postman mobile app
2. **Scan QR code** or import collection
3. **Same workflows:** Desktop and mobile identical
4. **Sync:** Collections across devices

### **Responsive Testing**
- Test with different User-Agent headers
- Verify mobile layouts
- Check touch interactions

---

## 🚨 **Common Issues & Solutions**

### **CSRF Token Missing**
**Error:** 403 Forbidden
**Solution:** Extract CSRF token from login page first

### **Session Expired**
**Error:** 302 Redirect to login
**Solution:** Login again to get new session

### **Invalid Form Data**
**Error:** 200 OK with error messages
**Solution:** Check response HTML for validation errors

### **Permission Denied**
**Error:** 403 Forbidden
**Solution:** Check user permissions (staff vs regular user)

---

## 📊 **Performance Testing**

### **Load Testing**
- **Multiple users:** Test concurrent voting
- **Poll creation:** Test multiple simultaneous polls
- **Database stress:** Test with large datasets

### **Security Testing**
- **SQL Injection:** Try malicious input
- **XSS Attempts:** Test script injection
- **CSRF Bypass:** Test without CSRF token
- **Authentication:** Test with invalid credentials

---

## 🎯 **Success Criteria**

### **Complete Test Coverage**
- [ ] All authentication flows tested
- [ ] All CRUD operations tested
- [ ] Error scenarios tested
- [ ] Performance benchmarks established
- [ ] Security vulnerabilities checked

### **Documentation Complete**
- [ ] Postman collection imported
- [ ] Environment variables set
- [ ] Test cases documented
- [ ] Team training completed

---

## 📚 **Additional Resources**

### **Django Documentation**
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django Forms](https://docs.djangoproject.com/en/4.2/topics/forms/)
- [Django Authentication](https://docs.djangoproject.com/en/4.2/topics/auth/default/)

### **Postman Documentation**
- [Postman Learning Center](https://learning.postman.com/)
- [Postman API Testing](https://learning.postman.com/docs/postman/scripts/test_examples/)
- [Postman Collections](https://learning.postman.com/docs/postman/collections/)

### **Testing Best Practices**
- [OWASP Testing Guide](https://owasp.org/www-project-secure-testing-guide/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [API Testing Standards](https://restfulapi.net/)

---

## 🎉 **Ready for Testing**

Your SimpleVote application is now fully documented and ready for comprehensive API testing with Postman!

**Key Benefits:**
- ✅ Complete endpoint documentation
- ✅ Ready-to-import Postman collection
- ✅ Step-by-step testing workflows
- ✅ Authentication flow guidance
- ✅ Error handling and debugging tips
- ✅ Performance and security testing guidelines

**Start testing your Django voting system with confidence!** 🚀
