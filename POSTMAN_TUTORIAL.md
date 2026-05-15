# 🎓 **Step-by-Step Postman Tutorial for Django Voting System**

## 📋 **Prerequisites**
- Django development server running (`python manage.py runserver`)
- Postman Desktop app installed
- Basic understanding of HTTP methods

---

## 🚀 **Step 1: Setting Up Postman Environment**

### 1.1 Create New Collection
1. Open Postman
2. Click **"Collections"** → **"+"** to create new collection
3. Name it: **"Django Voting System API"**
4. Add description: **"Complete API testing for Django voting system"**

### 1.2 Set Environment Variables
1. Go to **"Environments"** tab
2. Click **"+"** to create new environment
3. Name it: **"Django Dev"**
4. Add these variables:

| Variable | Initial Value | Description |
|----------|---------------|-------------|
| `baseUrl` | `http://localhost:8000` | Development server URL |
| `username` | `testuser` | Test username |
| `email` | `test@example.com` | Test email |
| `password` | `SecurePass123` | Test password |
| `csrf_token` | *leave empty* | Will be auto-populated |
| `session_cookie` | *leave empty* | Will be auto-populated |

### 1.3 Configure Collection Settings
1. Click on collection → **"Variables"** tab
2. Add same variables as initial values
3. Go to **"Authorization"** tab:
   - Type: **"No Auth"** (we'll handle session manually)
4. Go to **"Pre-request Script"** tab and add:

```javascript
// Auto-get CSRF token for POST requests
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

---

## 🔐 **Step 2: Authentication Setup**

### 2.1 Create Registration Request
1. **New Request** → Name: **"Register User"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/accounts/register/`
4. **Headers** tab:
   ```
   Content-Type: application/x-www-form-urlencoded
   ```
5. **Body** tab → **x-www-form-urlencoded**:
   ```
   username: {{username}}
   email: {{email}}
   password1: {{password}}
   password2: {{password}}
   first_name: Test
   last_name: User
   ```
6. **Tests** tab:
```javascript
pm.test("Registration successful", function() {
    pm.response.to.have.status(302); // Redirect on success
});

pm.test("No error messages", function() {
    const text = pm.response.text();
    pm.expect(text).to.not.include("error");
});
```

### 2.2 Create Login Request
1. **New Request** → Name: **"Login User"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/accounts/login/`
4. **Headers** tab:
   ```
   Content-Type: application/x-www-form-urlencoded
   ```
5. **Body** tab → **x-www-form-urlencoded**:
   ```
   username: {{username}}
   password: {{password}}
   csrfmiddlewaretoken: {{csrf_token}}
   ```
6. **Tests** tab:
```javascript
pm.test("Login successful", function() {
    pm.response.to.have.status(302);
});

// Extract session cookie
const cookies = pm.response.headers.get('Set-Cookie');
if (cookies) {
    pm.collectionVariables.set('session_cookie', cookies);
    console.log("Session cookie saved:", cookies);
}

pm.test("Session cookie set", function() {
    const cookies = pm.response.headers.get('Set-Cookie');
    pm.expect(cookies).to.exist;
});
```

### 2.3 Create CSRF Token Extractor
1. **New Request** → Name: **"Get CSRF Token"**
2. **Method**: `GET`
3. **URL**: `{{baseUrl}}/accounts/login/`
4. **Tests** tab:
```javascript
pm.test("CSRF token extracted", function() {
    const html = pm.response.text();
    const csrfMatch = html.match(/name='csrfmiddlewaretoken' value='([^']+)'/);
    if (csrfMatch) {
        pm.collectionVariables.set('csrf_token', csrfMatch[1]);
        console.log("CSRF Token:", csrfMatch[1]);
    }
    pm.expect(csrfMatch).to.exist;
});
```

---

## 📊 **Step 3: Testing Public Endpoints**

### 3.1 Test Landing Page
1. **New Request** → Name: **"Get Landing Page"**
2. **Method**: `GET`
3. **URL**: `{{baseUrl}}/`
4. **Tests** tab:
```javascript
pm.test("Landing page loads", function() {
    pm.response.to.have.status(200);
});

pm.test("Contains featured polls", function() {
    const text = pm.response.text();
    pm.expect(text).to.include("poll");
});
```

### 3.2 Test Poll List
1. **New Request** → Name: **"Get Poll List"**
2. **Method**: `GET`
3. **URL**: `{{baseUrl}}/voting/`
4. **Tests** tab:
```javascript
pm.test("Poll list loads", function() {
    pm.response.to.have.status(200);
});

pm.test("Contains poll data", function() {
    const text = pm.response.text();
    pm.expect(text).to.include("poll") || pm.expect(text).to.include("No polls");
});
```

### 3.3 Test Poll List with Filters
1. **Duplicate** previous request → Name: **"Get Poll List - Active Only"**
2. **URL**: `{{baseUrl}}/voting/?status=active`
3. **Tests** tab:
```javascript
pm.test("Filtered poll list loads", function() {
    pm.response.to.have.status(200);
});
```

---

## 🗳️ **Step 4: Testing Authenticated Endpoints**

### 4.1 Test Dashboard Access
1. **New Request** → Name: **"Get User Dashboard"**
2. **Method**: `GET`
3. **URL**: `{{baseUrl}}/accounts/dashboard/`
4. **Headers** tab:
   ```
   Cookie: {{session_cookie}}
   ```
5. **Tests** tab:
```javascript
pm.test("Dashboard accessible", function() {
    pm.response.to.have.status(200);
});

pm.test("Contains user data", function() {
    const text = pm.response.text();
    pm.expect(text).to.include("dashboard") || pm.expect(text).to.include("Welcome");
});
```

### 4.2 Test Poll Creation
1. **New Request** → Name: **"Create New Poll"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/voting/create/`
4. **Headers** tab:
   ```
   Content-Type: multipart/form-data
   Cookie: {{session_cookie}}
   ```
5. **Body** tab → **form-data**:
   ```
   title: Test Poll from Postman
   description: This is a test poll created via Postman
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
   choice_1: Python
   choice_2: JavaScript
   choice_3: Java
   csrfmiddlewaretoken: {{csrf_token}}
   ```
6. **Tests** tab:
```javascript
pm.test("Poll creation successful", function() {
    pm.response.to.have.status(302); // Redirect on success
});

pm.test("No error messages", function() {
    const text = pm.response.text();
    pm.expect(text).to.not.include("error");
});
```

### 4.3 Test Voting
1. **New Request** → Name: **"Vote in Poll"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/voting/poll/1/` (Assuming poll ID 1 exists)
4. **Headers** tab:
   ```
   Content-Type: application/x-www-form-urlencoded
   Cookie: {{session_cookie}}
   ```
5. **Body** tab → **x-www-form-urlencoded**:
   ```
   choice: 1
   csrfmiddlewaretoken: {{csrf_token}}
   ```
6. **Tests** tab:
```javascript
pm.test("Vote recorded", function() {
    pm.response.to.have.status(302);
});

pm.test("Success message present", function() {
    const text = pm.response.text();
    pm.expect(text).to.include("success") || pm.expect(text).to.include("vote");
});
```

---

## 💬 **Step 5: Testing Interactive Features**

### 5.1 Test Comment Addition
1. **New Request** → Name: **"Add Comment to Poll"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/voting/poll/1/comment/`
4. **Headers** tab:
   ```
   Content-Type: application/x-www-form-urlencoded
   Cookie: {{session_cookie}}
   ```
5. **Body** tab → **x-www-form-urlencoded**:
   ```
   content: Great poll! I love voting in Postman tests.
   csrfmiddlewaretoken: {{csrf_token}}
   ```

### 5.2 Test Poll Reactions
1. **New Request** → Name: **"Like Poll"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/voting/poll/1/react/like/`
4. **Headers** tab:
   ```
   Cookie: {{session_cookie}}
   ```

### 5.3 Test Profile Update
1. **New Request** → Name: **"Update User Profile"**
2. **Method**: `POST`
3. **URL**: `{{baseUrl}}/accounts/profile/`
4. **Headers** tab:
   ```
   Content-Type: multipart/form-data
   Cookie: {{session_cookie}}
   ```
5. **Body** tab → **form-data**:
   ```
   first_name: Updated
   last_name: Name
   bio: Updated bio from Postman
   location: Test City
   website: https://example.com
   email_notifications: true
   public_profile: true
   csrfmiddlewaretoken: {{csrf_token}}
   ```

---

## 🔧 **Step 6: Advanced Testing Techniques**

### 6.1 Create Test Flow
1. Select all requests in collection
2. Right-click → **"Save as"** → **"New Flow"**
3. Name it: **"Complete User Journey"**
4. Arrange in order: Register → Login → Get CSRF → Create Poll → Vote → Comment → Logout

### 6.2 Add Response Validation
Add these tests to key requests:
```javascript
// Check for Django errors
pm.test("No Django errors", function() {
    const text = pm.response.text();
    pm.expect(text).to.not.include("Page not found");
    pm.expect(text).to.not.include("Server Error");
    pm.expect(text).to.not.include("500");
});

// Response time check
pm.test("Response time acceptable", function() {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});

// Content type check
pm.test("Content type correct", function() {
    const contentType = pm.response.headers.get('Content-Type');
    if (pm.request.method === 'GET') {
        pm.expect(contentType).to.include('text/html');
    }
});
```

### 6.3 Batch Testing
1. **Collection Runner** → Select collection
2. **Iterations**: Set to 3 for testing multiple times
3. **Delay**: 1000ms between requests
4. **Run** and monitor results

---

## 🐛 **Step 7: Debugging Common Issues**

### 7.1 CSRF Token Issues
**Problem**: 403 Forbidden error
**Solution**: 
1. Run "Get CSRF Token" request first
2. Check that `{{csrf_token}}` variable is populated
3. Ensure token is included in all POST requests

### 7.2 Session Issues
**Problem**: Redirected to login page
**Solution**:
1. Check that `{{session_cookie}}` variable is set
2. Ensure Cookie header is included in authenticated requests
3. Re-run login request if session expired

### 7.3 Form Validation Errors
**Problem**: Form submission fails
**Solution**:
1. Check response body for error messages
2. Ensure all required fields are included
3. Verify data types and formats

### 7.4 Poll Not Found
**Problem**: 404 error when accessing poll
**Solution**:
1. Create a poll first
2. Check actual poll ID in database or admin panel
3. Update request URL with correct poll ID

---

## 📈 **Step 8: Performance Testing**

### 8.1 Load Testing Setup
1. **Collection Runner** → Set iterations to 50
2. Monitor response times
3. Check for server errors under load

### 8.2 Response Time Monitoring
Add to collection-level tests:
```javascript
if (pm.response.responseTime > 2000) {
    console.warn("Slow response detected:", pm.info.requestName, pm.response.responseTime + "ms");
}
```

---

## 🎯 **Step 9: Best Practices**

### 9.1 Organization
- Use folders to group related endpoints
- Name requests descriptively
- Add descriptions for complex requests

### 9.2 Documentation
- Document any special requirements
- Note dependencies between requests
- Include example responses in descriptions

### 9.3 Security Testing
- Test with invalid credentials
- Attempt to access unauthorized endpoints
- Test input validation with malformed data

### 9.4 Data Cleanup
- Create logout request to clean up session
- Use test data that won't conflict with real data
- Consider creating cleanup scripts

---

## 🚀 **Quick Start Checklist**

- [ ] Environment variables set
- [ ] CSRF token extractor working
- [ ] Registration request successful
- [ ] Login request successful
- [ ] Session cookie saved
- [ ] Dashboard accessible
- [ ] Poll creation working
- [ ] Voting functionality working
- [ ] Comments and reactions working
- [ ] Profile updates working

Run through this checklist to ensure your Postman setup is working correctly!

---

## 🎉 **Congratulations!**

You now have a complete Postman setup for testing the Django Voting System API. You can:

- ✅ Test all endpoints systematically
- ✅ Automate user journey testing
- ✅ Debug authentication and CSRF issues
- ✅ Perform load testing
- ✅ Validate responses and error handling

Happy testing! 🚀
