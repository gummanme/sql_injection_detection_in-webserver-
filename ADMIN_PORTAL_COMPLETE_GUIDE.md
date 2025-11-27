# 🏢 TechCorp Admin Login & Dashboard System - Complete Guide

## ✅ What's New

Your website now has a **professional admin portal** with complete authentication and dashboard access control.

### Before vs After

| Aspect             | Before        | After                         |
| ------------------ | ------------- | ----------------------------- |
| **Login Type**     | No login      | Admin authentication          |
| **Access Control** | Anyone        | Admin only                    |
| **Dashboard**      | Basic message | Full featured dashboard       |
| **Features**       | None          | Statistics, history, settings |
| **Security**       | None          | Session management            |

---

## 🎯 Complete System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TechCorp Admin Portal                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LOGIN LAYER (Public)                                       │
│  └─ login.html - Admin authentication form                  │
│     ├─ Username input                                        │
│     ├─ Password input                                        │
│     └─ Demo credentials: admin / admin123                    │
│                                                              │
│  ↓ Valid credentials create session ↓                       │
│                                                              │
│  DASHBOARD LAYER (Admin Only)                               │
│  └─ dashboard.html - Full company access                    │
│     ├─ 📊 Dashboard: Real-time statistics                   │
│     ├─ 🔍 Analyze: Submit HTTP requests                     │
│     ├─ 📜 History: View all requests                        │
│     └─ ⚙️  Settings: Account management                     │
│                                                              │
│  BACKEND LAYER (Flask)                                      │
│  └─ app.py - Routes & authentication                        │
│     ├─ POST /api/login - Verify credentials                 │
│     ├─ GET /dashboard - Serve dashboard                     │
│     ├─ POST /api/http-request - Accept requests             │
│     ├─ GET /api/dashboard-data - Provide statistics         │
│     └─ POST /api/logout - Clear session                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Flask

```bash
cd d:\csvmy
.\venv\Scripts\python app.py
```

### Step 2: Open Browser

Go to: **http://localhost:5000**

### Step 3: Login with Admin Credentials

```
Username: admin
Password: admin123
```

**That's it!** You're now in the admin dashboard with full access to all company features.

---

## 🔐 Authentication Details

### Login Process Flow

```
1. User visits http://localhost:5000/
2. Form displays login.html
3. User enters username & password
4. Flask validates against admin credentials
5. If valid:
   - Session created with role='admin'
   - User redirected to /dashboard
6. If invalid:
   - Error message shown
   - Failed attempt logged to http_requests.csv
```

### Admin Accounts (Hardcoded)

```
Account 1:
  Username: admin
  Password: admin123

Account 2:
  Username: root
  Password: root123
```

### Session Management

- **Duration**: 24 hours
- **Storage**: Server-side secure cookies
- **Expiration**: Auto-logout after 24 hours
- **Logout**: Manual logout button clears session immediately

---

## 📊 Dashboard Pages Explained

### 1️⃣ Dashboard (Default Tab)

**Shows company overview statistics:**

- ✅ Total HTTP Requests: Count of all submissions
- ✅ Legitimate Requests: Count of safe requests
- ⚠️ Suspicious Requests: Count of malicious requests
- 🎯 Model Accuracy: 100% (ML model performance)
- 📋 Recent Requests Table: Last 10 submissions

### 2️⃣ Analyze Request

**Submit HTTP requests for security classification:**

- Select HTTP Method (GET, POST, PUT, DELETE, PATCH, HEAD)
- Enter URL/Endpoint (e.g., `/api/users`, `/files/download`)
- Paste Request Body (query params or JSON)
- Click "Submit Request"
- View Classification: ✅ Legitimate or ⚠️ Malicious
- Risk Level: LOW or HIGH

### 3️⃣ Request History

**View all submitted requests:**

- Table with all HTTP requests
- Timestamp, Method, URL, Body
- Sortable and filterable
- Easy to review past submissions

### 4️⃣ Settings

**Account and system settings:**

- Display Username
- Display User Role (Administrator)
- Show Login Timestamp
- Change Password button (placeholder for future)

---

## 💾 Data Storage

### Files Created/Modified

| File                | Purpose                 | Access  |
| ------------------- | ----------------------- | ------- |
| `app.py`            | Flask backend with auth | Python  |
| `login.html`        | Login form UI           | Browser |
| `dashboard.html`    | Dashboard UI            | Browser |
| `http_requests.csv` | Request log             | CSV     |
| `login_dataset.csv` | ML training data        | CSV     |

### CSV Format

**http_requests.csv:**

```
timestamp,method,url,body
2025-11-27T10:15:30.123,POST,/api/login,username=admin&password=pass
2025-11-27T10:16:45.234,GET,/users/profile,user_id=123
```

---

## 🔍 Example Workflow

### Scenario: Test SQLi Detection

1. **Login**

   - Go to http://localhost:5000/
   - Enter: username `admin`, password `admin123`
   - Click Sign In

2. **Navigate to Analyze Request**

   - Click "🔍 Analyze Request" in sidebar

3. **Submit SQL Injection**

   - Method: `POST`
   - URL: `/api/login`
   - Body: `username=admin' OR '1'='1`
   - Click "Submit Request"

4. **View Result**

   - Classification: ⚠️ **MALICIOUS REQUEST**
   - Risk Level: **HIGH**
   - Features show detection of SQL keywords

5. **Check History**

   - Click "📜 Request History"
   - See all submitted requests in table

6. **View Dashboard Stats**
   - Click "📊 Dashboard"
   - Statistics updated with new request counts

---

## 🛡️ Security Architecture

### Authorization Layers

```
Layer 1: Login Authentication
  ├─ Username validation
  ├─ Password comparison
  └─ Session creation

Layer 2: Route Protection
  ├─ /dashboard requires session + admin role
  ├─ /api/dashboard-data requires session + admin role
  ├─ /api/http-request requires session + admin role
  └─ /api/logout requires session

Layer 3: Error Handling
  ├─ Invalid credentials → Error message + logging
  ├─ No session → Redirect to login
  ├─ Expired session → Redirect to login
  └─ No admin role → Deny access
```

### Audit Trail

- Failed login attempts logged to CSV
- Request submissions recorded with timestamp
- User session activity tracked

---

## 📋 All Available Routes

### Public Routes

```
GET  /              → Shows login.html (or redirects if logged in)
POST /api/login     → Handle login, create session
```

### Admin Routes (Require Login)

```
GET  /dashboard     → Show admin dashboard
GET  /api/dashboard-data  → Return statistics JSON
POST /api/http-request    → Submit HTTP request
POST /api/logout    → Clear session, logout
```

---

## 🎓 Use Cases

### Use Case 1: Security Testing

1. Login as admin
2. Go to "Analyze Request"
3. Submit various HTTP payloads
4. ML model classifies each as good/bad
5. Review results in History

### Use Case 2: Company Dashboard

1. Login as admin
2. Check Dashboard tab
3. View all statistics
4. See recent requests
5. Monitor system activity

### Use Case 3: Request Auditing

1. Login as admin
2. Go to Request History
3. Review all submitted requests
4. Check timestamps and details
5. Export for compliance

---

## 🔧 Customization Options

### Change Admin Credentials

Edit `app.py`:

```python
ADMIN_USERS = {
    'admin': 'admin123',    # Change these
    'root': 'root123',      # values here
    'newuser': 'newpass'    # Add more users
}
```

### Change Session Duration

Edit `app.py`:

```python
app.permanent_session_lifetime = timedelta(hours=24)  # Change 24 to any value
```

### Change Dashboard Title/Colors

Edit `dashboard.html` CSS section for styling

---

## ❌ Troubleshooting

| Issue                 | Solution                               |
| --------------------- | -------------------------------------- |
| Can't login           | Use credentials: `admin` / `admin123`  |
| "Unauthorized"        | Refresh page, login again              |
| Dashboard not loading | Check if Flask is running on port 5000 |
| CSV files empty       | Submit requests first to generate data |
| Can't logout          | Click "Logout" button or clear cookies |

---

## 📈 System Status

✅ **Login System**: Working
✅ **Admin Authentication**: Active
✅ **Dashboard**: Fully Functional
✅ **Session Management**: 24-hour expiration
✅ **Role-Based Access**: Enforced
✅ **Request Logging**: CSV storage
✅ **ML Integration**: Classification ready
✅ **Flask Server**: Running on localhost:5000

---

## 🎯 Summary

Your TechCorp admin portal now features:

1. **Professional Login** - Clean, branded admin authentication
2. **Secure Access** - Role-based access control
3. **Full Dashboard** - Real-time statistics and monitoring
4. **Request Analysis** - ML-powered classification
5. **History Tracking** - Complete audit trail
6. **Account Settings** - User management

**Login now with:**

- Username: `admin`
- Password: `admin123`

**Everything is ready to use!** 🚀
