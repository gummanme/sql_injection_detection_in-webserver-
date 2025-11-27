# Admin Login & Dashboard System

## Overview

Your website now features a complete admin authentication system with a professional company dashboard. Only authorized admins can access full company features.

## Features Implemented

### 1. Admin Login Page (`login.html`)

- Professional two-column design with company branding
- Admin credentials form with username and password
- Demo credentials displayed for easy testing
- Session management with secure cookies
- Error/success alerts

**Demo Credentials:**

```
Username: admin
Password: admin123
```

Alternative admin account:

```
Username: root
Password: root123
```

### 2. Admin Dashboard (`dashboard.html`)

After successful admin login, users access a full-featured company dashboard with:

#### Sidebar Navigation

- 📊 Dashboard
- 🔍 Analyze Request
- 📜 Request History
- ⚙️ Settings

#### Dashboard Page

- **Statistics Cards**: Total requests, legitimate/suspicious, model accuracy
- **Recent Requests Table**: Latest submitted HTTP requests
- Real-time data loading from backend

#### Analyze Request Page

- Form to submit HTTP requests for security analysis
- Fields: Method, URL, Body
- Results show classification and risk level
- Saves to CSV automatically

#### Request History Page

- Table of all submitted HTTP requests
- Sortable and searchable data

#### Settings Page

- Account information display
- Login timestamp
- Change password button (placeholder)

### 3. Backend Routes (Flask)

#### Authentication Routes

- `GET /` - Login page (redirects to dashboard if already logged in)
- `POST /api/login` - Handle admin authentication
- `POST /api/logout` - Clear session and logout

#### Dashboard Routes

- `GET /dashboard` - Admin dashboard (requires authentication)
- `GET /api/dashboard-data` - Get dashboard statistics (JSON)

#### HTTP Request Routes

- `POST /api/http-request` - Submit HTTP request for analysis (admin only)

#### Security Features

- Session-based authentication
- Role-based access control (admin role)
- 24-hour session expiration
- Unauthorized access redirects to login
- Failed login attempts logged to CSV

### 4. Updated Flask App (`app.py`)

**New Features:**

```python
- Session management with secure secret key
- Admin user credentials dictionary
- Role-based authorization checks
- Failed login attempt logging
- Dashboard data aggregation
- CSV statistics calculation
```

## User Experience Flow

### 1. Initial Access

```
User visits http://localhost:5000/
↓
Shows login.html with admin login form
↓
User enters credentials
```

### 2. Valid Admin Login

```
Credentials match (admin/admin123)
↓
Session created with role='admin'
↓
Redirects to /dashboard
↓
Shows full company dashboard
```

### 3. Failed Login

```
Credentials don't match
↓
Error message displayed
↓
Failed attempt logged to CSV
↓
User stays on login page
```

### 4. Dashboard Access

Once logged in, admin can:

- View real-time statistics
- Analyze HTTP requests
- View request history
- Manage account settings
- Logout

## Security Features

1. **Session Management**

   - Secure session key generation using `secrets.token_hex(32)`
   - 24-hour session expiration
   - Session invalidation on logout

2. **Access Control**

   - All admin routes check for valid session
   - Unauthorized users redirected to login
   - Role-based authorization ('admin')

3. **Data Protection**

   - Failed login attempts logged
   - Credentials validated against server-side dictionary
   - No passwords in CSV files

4. **Authentication**
   - Username and password verification
   - Session cookies (HTTPOnly in production)
   - Secure logout functionality

## File Structure

```
d:\csvmy\
├── app.py (Updated with auth + dashboard routes)
├── templates/
│   ├── login.html (Admin login form)
│   └── dashboard.html (Admin dashboard)
├── http_requests.csv (Request log)
├── login_dataset.csv (ML training data)
└── ...
```

## Running the System

**Start Flask Server:**

```bash
cd d:\csvmy
.\venv\Scripts\python app.py
```

**Access in Browser:**

- Login: http://localhost:5000/
- Dashboard: http://localhost:5000/dashboard (auto-redirects if logged in)

## Testing

### Test 1: Valid Admin Login

1. Go to http://localhost:5000/
2. Username: `admin`
3. Password: `admin123`
4. Expected: Redirects to dashboard

### Test 2: Invalid Credentials

1. Go to http://localhost:5000/
2. Username: `user`
3. Password: `wrong`
4. Expected: Error message, failed attempt logged

### Test 3: Dashboard Access

1. After logging in, click different sidebar menu items
2. Expected: Dashboard loads statistics, forms work, history displays

### Test 4: Logout

1. Click "Logout" button
2. Expected: Redirects to login page, session cleared

## Admin Dashboard Features

| Feature              | Status | Details                |
| -------------------- | ------ | ---------------------- |
| Login Authentication | ✅     | Admin-only access      |
| Session Management   | ✅     | 24-hour expiration     |
| Real-time Dashboard  | ✅     | Live statistics        |
| Request Submission   | ✅     | HTTP method/URL/body   |
| Request History      | ✅     | All submitted requests |
| Role-based Access    | ✅     | Admin role enforcement |
| Logout Functionality | ✅     | Session clearing       |

## Next Steps (Optional)

1. Add multi-user support with database
2. Implement password hashing (bcrypt)
3. Add 2FA (Two-Factor Authentication)
4. Create admin user management panel
5. Add request filtering/search
6. Export reports feature
7. Real-time notifications
8. Audit logging

## Status

✅ **Admin Login System Complete**
✅ **Professional Dashboard Implemented**
✅ **Session Management Working**
✅ **Flask Server Running** (localhost:5000)
✅ **Role-Based Access Control Active**

---

**Demo Ready!** Login with:

- Username: `admin`
- Password: `admin123`
