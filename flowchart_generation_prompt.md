# AI Flow Chart Generation Prompt for Django Voting System Backend

## 🎯 **Objective**
Create a comprehensive, beautiful, and detailed flow chart that visualizes all backend processes of the Django voting system. The flow chart should be technically accurate yet easily understandable for both technical and non-technical viewers.

## 🏗️ **System Architecture Overview**

The Django voting system is built with:
- **Framework**: Django 4.2 with Python
- **Database**: PostgreSQL with Django ORM
- **Architecture**: MVT (Model-View-Template) pattern
- **Authentication**: Custom user model with Django's auth system
- **Apps**: Two main applications - `accounts` and `voting`

## 📊 **Flow Chart Requirements**

### **Main Components to Include:**

#### **1. Request Flow Layer**
- **Entry Point**: Django WSGI Application
- **URL Routing**: Main project URLs → App-specific URLs
- **Middleware Stack**: Security, Session, CSRF, Auth, Messages
- **Request Processing**: View functions/class-based views

#### **2. User Management System (Accounts App)**
- **User Registration Flow**:
  - Form validation → Custom user creation → Profile creation → Activity tracking → Auto-login → Dashboard redirect
- **Authentication Flow**:
  - Login form → Credentials validation → Session creation → Activity logging → Dashboard access
- **User Profile Management**:
  - Profile update → Avatar upload → Preference settings → Activity tracking
- **User Activity Tracking**:
  - Login/logout tracking → Poll creation tracking → Vote casting tracking → Profile updates

#### **3. Voting System Core (Voting App)**
- **Poll Management Flow**:
  - Poll creation → Choice creation → Category assignment → Tag management → Validation → Database storage
- **Voting Process Flow**:
  - Poll retrieval → User eligibility check → Vote validation → Vote recording → Result calculation → Activity logging
- **Poll Status Management**:
  - Scheduled activation → Real-time status checking → Automatic closing → Result publication

#### **4. Database Layer**
- **Models Relationships**:
  - User ↔ UserProfile (One-to-One)
  - User ↔ Poll (One-to-Many)
  - User ↔ Vote (One-to-Many)
  - Poll ↔ Choice (One-to-Many)
  - Poll ↔ Vote (One-to-Many)
  - Poll ↔ Category (Many-to-One)
  - Poll ↔ Comments (One-to-Many)
  - Poll ↔ Reactions (One-to-Many)

#### **5. Data Validation & Security**
- **Input Validation**: Form validation, Model clean methods
- **Permission Checks**: Login required, Poll ownership, Voting eligibility
- **Security Measures**: CSRF protection, SQL injection prevention, XSS protection

#### **6. Response Generation**
- **Template Rendering**: Django template engine with context
- **JSON Responses**: AJAX endpoints for dynamic interactions
- **Static File Serving**: CSS, JavaScript, Images
- **Media File Handling**: User uploads, avatars

## 🎨 **Visual Design Requirements**

### **Color Scheme & Styling:**
- **Primary Colors**: Django blue (#092e20) and green (#4caf50)
- **Secondary Colors**: Orange for voting, Purple for user management, Teal for database
- **Background**: Clean white with subtle gradients
- **Text**: Dark gray for readability

### **Layout Structure:**
- **Top Section**: Request entry points and middleware
- **Middle Layers**: Application logic (accounts, voting)
- **Bottom Section**: Database and response generation
- **Side Annotations**: Detailed explanations for each process

### **Flow Chart Elements:**
- **Rounded Rectangles**: Processes and functions
- **Diamonds**: Decision points and validations
- **Cylinders**: Database operations
- **Arrows**: Data flow direction
- **Icons**: Small symbols for different operations (👤 user, 🗳️ vote, 📊 data)

## 📝 **Side Annotations Requirements**

For each major process block, include:

### **User Registration Process:**
```
🔐 User Registration
- Validates email uniqueness and password strength
- Creates custom User model with extended fields
- Automatically creates UserProfile and UserActivity records
- Logs user in immediately after successful registration
- Redirects to personalized dashboard
```

### **Poll Creation Process:**
```
📋 Poll Creation
- Validates poll dates and voting rules
- Supports categories and tags for organization
- Allows multiple voting options and restrictions
- Tracks creator and timestamps for audit trail
- Sets up automatic activation/closing schedule
```

### **Voting Process:**
```
🗳️ Vote Casting
- Checks poll active status and user eligibility
- Enforces voting limits and restrictions
- Records vote with timestamp and user info
- Updates real-time vote counts and percentages
- Logs activity for user history and analytics
```

### **Database Operations:**
```
💾 Data Persistence
- PostgreSQL database with ACID compliance
- Django ORM for type-safe database operations
- Automatic migrations for schema changes
- Optimized queries with select_related and prefetch_related
- Indexes for performance on frequently accessed fields
```

## 🔧 **Technical Details to Highlight**

### **Middleware Stack:**
1. SecurityMiddleware (HTTPS, HSTS)
2. SessionMiddleware (User sessions)
3. CommonMiddleware (URL handling)
4. CsrfViewMiddleware (CSRF protection)
5. AuthenticationMiddleware (User authentication)
6. MessageMiddleware (Flash messages)
7. XFrameOptionsMiddleware (Clickjacking protection)

### **Key Features:**
- **Real-time Status**: Polls automatically activate/deactivate based on dates
- **Vote Integrity**: One vote per user per poll (configurable)
- **Rich Interactions**: Comments, reactions, and activity tracking
- **Search & Filter**: Advanced poll discovery with categories and tags
- **Responsive Design**: Mobile-friendly interface with Bootstrap

### **Security Measures:**
- Password hashing with Django's built-in validators
- CSRF tokens on all forms
- SQL injection prevention through ORM
- XSS protection in templates
- User permission checks

## 📈 **Performance Optimizations**

Show in the flow chart:
- Database query optimization
- Select_related and prefetch_related usage
- Pagination for large datasets
- Caching strategies (if implemented)
- Efficient file upload handling

## 🎯 **Final Output Requirements**

The flow chart should be:
- **Comprehensive**: Cover all major backend processes
- **Readable**: Clear labels and logical flow
- **Beautiful**: Professional color scheme and modern design
- **Educational**: Side annotations that explain each process
- **Technical**: Accurate representation of Django's MVT architecture
- **Scalable**: Show how the system can handle growth

## 📐 **Dimensions & Format**
- **Size**: Large enough to show detail (recommended 1920x1080 or larger)
- **Format**: High-resolution PNG or SVG for scalability
- **Layout**: Vertical flow with horizontal process branches
- **Typography**: Clean, modern fonts with good readability

Generate this flow chart with attention to both technical accuracy and visual appeal, making it suitable for documentation, presentations, or educational purposes about Django web development and voting system architecture.
