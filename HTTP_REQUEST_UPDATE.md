# HTTP Request Format Update

## Overview

The system has been updated to accept HTTP request format (method, URL, body) instead of username/password credentials.

## Changes Made

### 1. Flask Web App (`app.py`)

**Changes:**

- Renamed `LOGIN_CSV` → `REQUEST_CSV` (now `http_requests.csv`)
- CSV header changed from `['timestamp', 'username', 'password']` → `['timestamp', 'method', 'url', 'body']`
- Updated `/api/login` endpoint to accept:
  - `method`: HTTP method (GET, POST, PUT, DELETE, etc.)
  - `url`: Request endpoint/URL
  - `body`: Request body content

**Data Flow:**

1. Accepts HTTP request via form
2. Saves to `http_requests.csv` with timestamp
3. Appends to `login_dataset.csv` for ML model classification

### 2. Streamlit App (`app_streamlit.py`)

**Changes:**

- Updated feature extraction to work with HTTP request bodies instead of username/password
- Renamed function `load_credentials_from_csv()` → `load_requests_from_csv()`
- Updated classification page with new form fields:
  - HTTP Method selector (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
  - URL/Endpoint text input
  - Request Body text area (multi-line)

**Classification Process:**

1. User enters method, URL, and request body
2. App extracts features from the body
3. ML model classifies as "good" or "bad"
4. Displays risk level and confidence score
5. Shows feature analysis breakdown

### 3. HTML Form (`templates/index.html`)

**Changes:**

- Updated form title: "Login to Your Account" → "Submit HTTP Request"
- Replaced username/password fields with:
  - HTTP Method dropdown selector
  - URL/Endpoint text input
  - Request Body textarea (multi-line)
- Updated left section heading and features list
- Updated JavaScript to handle new form fields

**Data Submission:**

- Form sends HTTP POST request with method, URL, body, and timestamp
- Backend saves to `http_requests.csv`
- Records auto-appended to `login_dataset.csv`

## CSV File Format

### http_requests.csv

```
timestamp,method,url,body
2025-11-27T10:15:30.123456,POST,/api/login,username=admin&password=pass123
2025-11-27T10:16:45.234567,GET,/users/profile,
2025-11-27T10:17:52.345678,POST,/api/data,"select * from users; --"
```

### login_dataset.csv (Updated)

```
method,endpoint,body,f1,f2,f3,f4,f5,f6,label
POST,/api/login,username=admin&password=pass123,0,0,0,0,0,0,good
GET,/users/profile,../../../etc/passwd,0,0,1,0,0,0,bad
```

## Feature Detection

The ML model analyzes request bodies for:

1. **Body Length**: Overall character count
2. **Special Characters**: Detects `'`, `"`, `-`, `;`, `*`
3. **SQL Keywords**: Detects injection patterns (UNION, SELECT, DROP, INSERT, UPDATE, DELETE, EXEC, SCRIPT)
4. **Path Traversal**: Detects `..` patterns
5. **Slashes**: Counts forward slash occurrences

## How to Use

### Via Website (http://localhost:5000)

1. Select HTTP method from dropdown
2. Enter URL/endpoint (e.g., `/api/login`)
3. Enter request body (e.g., `username=admin&password=pass`)
4. Click "Submit Request"
5. Data is saved to CSV files

### Via Streamlit (http://localhost:8501)

1. Go to "Classify Credentials" page
2. Select HTTP method
3. Enter URL/endpoint
4. Paste request body
5. Click "Classify"
6. View risk assessment and feature analysis
7. Optionally save to history

## Running the Applications

### Flask Website

```bash
cd d:\csvmy
.\venv\Scripts\python app.py
# Opens at http://localhost:5000
```

### Streamlit Dashboard

```bash
cd d:\csvmy
.\venv\Scripts\streamlit run app_streamlit.py
# Opens at http://localhost:8501
```

## Example Usage

### Example 1: Legitimate GET Request

- **Method**: GET
- **URL**: `/users/profile`
- **Body**: `user_id=123`
- **Expected Classification**: ✅ GOOD (Low Risk)

### Example 2: SQL Injection Attempt

- **Method**: POST
- **URL**: `/api/login`
- **Body**: `username=admin' OR '1'='1`
- **Expected Classification**: ❌ BAD (High Risk)

### Example 3: Path Traversal Attack

- **Method**: GET
- **URL**: `/files/download`
- **Body**: `filepath=../../../etc/passwd`
- **Expected Classification**: ❌ BAD (High Risk)

## Files Modified

- ✅ `app.py` - Flask backend
- ✅ `app_streamlit.py` - Streamlit dashboard
- ✅ `templates/index.html` - Web form
- ✅ New: `http_requests.csv` - Request storage
- ✅ Updated: `login_dataset.csv` - ML training data

## Status

✅ **All components updated and tested**
✅ **Flask app running on port 5000**
✅ **Streamlit app running on port 8501**
✅ **HTTP request format fully integrated**
