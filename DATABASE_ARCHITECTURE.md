# 🗄️ Database Architecture Documentation

## 📊 **Database Overview**

### **Database System**
- **Type:** PostgreSQL 14+
- **Connection:** psycopg2-binary adapter
- **ORM:** Django ORM (Object-Relational Mapper)
- **Migration System:** Django Migrations
- **Character Set:** UTF-8
- **Timezone:** UTC (configured in Django settings)

---

## 🏗️ **Database Schema Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        SIMPLEVOTE DATABASE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   ACCOUNTS     │  │    VOTING      │  │   DJANGO       │  │
│  │                 │  │                 │  │   BUILTIN       │  │
│  │                 │  │                 │  │                 │  │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │
│  │ │    USER     │ │  │ │    POLL      │ │  │ │    AUTH_USER │ │  │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │
│  │        │        │        │        │  │        │        │  │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │
│  │ │USER_PROFILE │ │  │ │   CHOICE    │ │  │ │     SESSION  │ │  │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │
│  │        │        │        │        │  │        │        │  │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │
│  │ │USER_ACTIVITY│ │  │ │     VOTE    │ │  │ │  CONTENTTYPE │ │  │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │
│  │        │        │        │        │  │        │        │  │
│  │                 │  │ ┌─────────────┐ │  │                 │  │
│  │                 │  │ │   CATEGORY   │ │  │                 │  │
│  │                 │  │ └─────────────┘ │  │                 │  │
│  │                 │  │        │        │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 **Table Relationships**

### **Primary Key Relationships**
```
USER (1) ──────── (M) USER_PROFILE
USER (1) ──────── (M) POLL (creator)
USER (1) ──────── (M) VOTE (voter)
POLL (1) ──────── (M) CHOICE
POLL (1) ──────── (M) VOTE
POLL (1) ──────── (M) POLL_COMMENT
POLL (1) ──────── (M) POLL_REACTION
CHOICE (1) ──────── (M) VOTE
CATEGORY (1) ──────── (M) POLL
USER (1) ──────── (M) USER_ACTIVITY
```

### **Foreign Key Constraints**
```sql
-- User to UserProfile
ALTER TABLE accounts_userprofile 
ADD CONSTRAINT user_profile_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES accounts_user(id);

-- Poll to Creator
ALTER TABLE voting_poll 
ADD CONSTRAINT poll_creator_id_fkey 
FOREIGN KEY (creator_id) REFERENCES accounts_user(id);

-- Vote to User and Choice
ALTER TABLE voting_vote 
ADD CONSTRAINT vote_voter_id_fkey 
FOREIGN KEY (voter_id) REFERENCES accounts_user(id),
ADD CONSTRAINT vote_choice_id_fkey 
FOREIGN KEY (choice_id) REFERENCES voting_choice(id);

-- Choice to Poll
ALTER TABLE voting_choice 
ADD CONSTRAINT choice_poll_id_fkey 
FOREIGN KEY (poll_id) REFERENCES voting_poll(id);

-- Category to Poll
ALTER TABLE voting_poll 
ADD CONSTRAINT poll_category_id_fkey 
FOREIGN KEY (category_id) REFERENCES voting_category(id);
```

---

## 🏛️ **Table Structures**

### **1. Accounts App Tables**

#### **accounts_user** (Custom User Model)
```sql
CREATE TABLE accounts_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    password VARCHAR(128) NOT NULL,
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_user_username ON accounts_user(username);
CREATE INDEX idx_user_email ON accounts_user(email);
CREATE INDEX idx_user_active ON accounts_user(is_active);
```

#### **accounts_userprofile** (Extended User Information)
```sql
CREATE TABLE accounts_userprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    bio TEXT,
    location VARCHAR(100),
    website VARCHAR(200),
    avatar VARCHAR(100),
    birth_date DATE,
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_userprofile_user_id ON accounts_userprofile(user_id);
```

#### **accounts_useractivity** (User Activity Tracking)
```sql
CREATE TABLE accounts_useractivity (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL,
    description TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Indexes
CREATE INDEX idx_useractivity_user_id ON accounts_useractivity(user_id);
CREATE INDEX idx_useractivity_timestamp ON accounts_useractivity(timestamp);
CREATE INDEX idx_useractivity_type ON accounts_useractivity(activity_type);
```

### **2. Voting App Tables**

#### **voting_category** (Poll Categories)
```sql
CREATE TABLE voting_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#007bff',
    icon VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_category_slug ON voting_category(slug);
```

#### **voting_poll** (Main Poll Entity)
```sql
CREATE TABLE voting_poll (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    creator_id INTEGER NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES voting_category(id) ON DELETE SET NULL,
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    is_closed BOOLEAN DEFAULT FALSE,
    allow_multiple_choices BOOLEAN DEFAULT FALSE,
    anonymous_voting BOOLEAN DEFAULT FALSE,
    tags TEXT, -- Stored as comma-separated values
    max_choices INTEGER DEFAULT 10
);

-- Indexes
CREATE INDEX idx_poll_creator ON voting_poll(creator_id);
CREATE INDEX idx_poll_category ON voting_poll(category_id);
CREATE INDEX idx_poll_created ON voting_poll(created_at);
CREATE INDEX idx_poll_active ON voting_poll(is_active);
CREATE INDEX idx_poll_dates ON voting_poll(start_date, end_date);
```

#### **voting_choice** (Poll Options)
```sql
CREATE TABLE voting_choice (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER NOT NULL REFERENCES voting_poll(id) ON DELETE CASCADE,
    text VARCHAR(500) NOT NULL,
    order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_choice_poll ON voting_choice(poll_id);
CREATE INDEX idx_choice_order ON voting_choice(poll_id, "order");
```

#### **voting_vote** (User Votes)
```sql
CREATE TABLE voting_vote (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER NOT NULL REFERENCES voting_poll(id) ON DELETE CASCADE,
    choice_id INTEGER NOT NULL REFERENCES voting_choice(id) ON DELETE CASCADE,
    voter_id INTEGER NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Unique constraint (one vote per user per poll)
CREATE UNIQUE INDEX idx_vote_unique ON voting_vote(poll_id, voter_id);

-- Indexes
CREATE INDEX idx_vote_poll ON voting_vote(poll_id);
CREATE INDEX idx_vote_voter ON voting_vote(voter_id);
CREATE INDEX idx_vote_voted_at ON voting_vote(voted_at);
```

#### **voting_pollcomment** (Poll Comments)
```sql
CREATE TABLE voting_pollcomment (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER NOT NULL REFERENCES voting_poll(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Indexes
CREATE INDEX idx_comment_poll ON voting_pollcomment(poll_id);
CREATE INDEX idx_comment_user ON voting_pollcomment(user_id);
CREATE INDEX idx_comment_created ON voting_pollcomment(created_at);
```

#### **voting_pollreaction** (Poll Reactions)
```sql
CREATE TABLE voting_pollreaction (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER NOT NULL REFERENCES voting_poll(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    reaction_type VARCHAR(20) NOT NULL, -- 'like', 'love', 'laugh'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Unique constraint (one reaction per user per poll per type)
CREATE UNIQUE INDEX idx_reaction_unique ON voting_pollreaction(poll_id, user_id, reaction_type);

-- Indexes
CREATE INDEX idx_reaction_poll ON voting_pollreaction(poll_id);
CREATE INDEX idx_reaction_user ON voting_pollreaction(user_id);
```

---

## 🔍 **Django Built-in Tables**

### **django_migrations** (Migration History)
```sql
CREATE TABLE django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **django_session** (User Sessions)
```sql
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);
```

### **django_contenttype** (Content Types)
```sql
CREATE TABLE django_contenttype (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);
```

---

## 📊 **Data Flow Analysis**

### **1. User Registration Flow**
```
POST /accounts/register/
├── Validate form data
├── Create accounts_user record
├── Create accounts_userprofile record
├── Log user_activity (registration)
├── Create django_session record
└── Redirect to dashboard
```

### **2. Poll Creation Flow**
```
POST /voting/create/
├── Validate poll data
├── Create voting_poll record
├── Create voting_choice records (multiple)
├── Log user_activity (poll_created)
└── Redirect to poll detail
```

### **3. Voting Flow**
```
POST /voting/poll/{id}/vote/
├── Validate user authentication
├── Check if user already voted
├── Create voting_vote record
├── Update choice vote counts (via ORM)
├── Log user_activity (vote_cast)
└── Redirect to poll results
```

---

## 🔧 **Performance Optimizations**

### **Database Indexes**
- **Primary Keys:** Automatically indexed by PostgreSQL
- **Foreign Keys:** Indexed for join performance
- **Query Fields:** Indexed on frequently filtered columns
- **Composite Indexes:** For complex queries

### **Query Optimization**
```python
# Efficient poll listing with related data
Poll.objects.select_related('creator', 'category')
         .annotate(vote_count=Count('vote'))
         .order_by('-created_at')

# Efficient user activity tracking
UserActivity.objects.filter(user_id=user.id)
               .order_by('-timestamp')[:10]

# Efficient vote counting
Choice.objects.filter(poll_id=poll.id)
         .annotate(vote_count=Count('vote'))
         .order_by('-vote_count')
```

### **Connection Pooling**
- **Default:** Django connection pooling
- **Settings:** Configurable in settings.py
- **Benefit:** Reuses database connections

---

## 🔐 **Security Considerations**

### **Data Integrity**
- **Foreign Key Constraints:** Prevent orphaned records
- **Unique Constraints:** Prevent duplicate votes
- **Check Constraints:** Validate data at database level
- **Cascade Deletes:** Maintain referential integrity

### **Access Control**
- **User Isolation:** Users see only their data
- **Staff Permissions:** Admin-only endpoints
- **Session Security:** Secure session management
- **CSRF Protection:** Form submission security

---

## 📈 **Scaling Considerations**

### **Database Scaling**
- **Read Replicas:** For high-read scenarios
- **Partitioning:** For large tables (votes, activities)
- **Archiving:** Historical data management
- **Connection Limits:** Resource management

### **Application Scaling**
- **Caching:** Django cache framework ready
- **CDN:** Static asset distribution
- **Load Balancing:** Multiple app servers
- **Database Sharding:** For massive scale

---

## 🔄 **Migration Strategy**

### **Current Migrations**
```
accounts/
├── 0001_initial.py
└── (future migrations)

voting/
├── 0001_initial.py
└── 0002_category_alter_vote_unique_together_and_more.py
```

### **Migration Commands**
```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Fake migration (for data migrations)
python manage.py migrate --fake
```

---

## 📊 **Database Statistics**

### **Expected Growth**
- **Users:** Linear growth with user acquisition
- **Polls:** Proportional to active users
- **Votes:** Exponential with poll popularity
- **Activities:** High-frequency tracking data

### **Storage Estimates**
```
Users (1,000) × 2KB = 2MB
Polls (10,000) × 1KB = 10MB
Choices (50,000) × 100B = 5MB
Votes (100,000) × 50B = 5MB
Comments (20,000) × 200B = 4MB
Activities (500,000) × 100B = 50MB

Total Estimated: ~76MB (excluding indexes and overhead)
```

---

## 🛠️ **Maintenance Tasks**

### **Regular Maintenance**
- **Session Cleanup:** Remove expired sessions
- **Activity Archiving:** Move old activities to archive
- **Statistics Updates:** Refresh materialized views
- **Index Rebuilding:** Optimize query performance

### **Backup Strategy**
- **Full Backups:** Daily database dumps
- **Incremental:** Transaction log backups
- **Point-in-Time:** Restore capability
- **Testing:** Regular restore drills

---

## 🎯 **Database Health Monitoring**

### **Key Metrics**
- **Connection Count:** Active database connections
- **Query Performance:** Slow query identification
- **Index Usage:** Index effectiveness analysis
- **Table Sizes:** Storage monitoring
- **Lock Waits:** Concurrency issues

### **Alerting**
- **Connection Errors:** Database connectivity
- **Slow Queries:** Performance degradation
- **Storage Limits:** Disk space warnings
- **Replication Lag:** Read replica delays

---

This database architecture provides a solid foundation for a scalable, secure, and maintainable voting system with excellent performance characteristics.
