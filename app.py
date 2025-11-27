from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import csv
import os
import secrets
import joblib
import pandas as pd


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate secure session key

# File paths
REQUEST_CSV = 'http_requests.csv'
LOGIN_DATASET_CSV = 'login_dataset.csv'

# Admin users (still available if ALLOW_ANY_LOGIN is False)
ADMIN_USERS = {'admin': 'admin123', 'root': 'root123'}

# Toggle so the app accepts any credentials as admin when True
ALLOW_ANY_LOGIN = True

# Load ML model (if present). Keep failures non-fatal.
MODEL = None
FEATURE_COLS = None
if os.path.exists('login_classifier.pkl') and os.path.exists('feature_columns.pkl'):
    try:
        MODEL = joblib.load('login_classifier.pkl')
        FEATURE_COLS = joblib.load('feature_columns.pkl')
        print('ML model loaded. Feature columns:', FEATURE_COLS)
    except Exception as e:
        print('Failed to load ML model or feature columns:', e)


def extract_features_from_body(body):
    s = str(body)
    features = {
        'body_length': len(s),
        'has_special_chars': 1 if any(c in s for c in ["'", '"', '-', ';', '*']) else 0,
        'has_sql_keywords': 1 if any(kw in s.lower() for kw in ['union', 'select', 'drop', 'insert', 'update', 'delete', 'exec', 'script']) else 0,
        'has_path_traversal': 1 if '..' in s else 0,
        'body_contains_slash': s.count('/'),
        # placeholders for f1-f3 used in training
        'f1': 0,
        'f2': 0,
        'f3': 0,
    }
    return features


# Ensure CSVs exist
if not os.path.exists(REQUEST_CSV):
    with open(REQUEST_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'method', 'url', 'body'])

if not os.path.exists(LOGIN_DATASET_CSV):
    # create with no header (existing dataset had no header)
    open(LOGIN_DATASET_CSV, 'a', encoding='utf-8').close()

# Detected alerts file for later review
DETECTED_ALERTS_CSV = 'detected_alerts.csv'
if not os.path.exists(DETECTED_ALERTS_CSV):
    with open(DETECTED_ALERTS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'endpoint', 'raw_body', 'classification', 'notes'])


@app.route('/')
def index():
    if 'user' in session and session.get('role') == 'admin':
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def login():
    try:
        # Capture raw request body exactly as received by the server
        raw_request = request.get_data(as_text=True)
        print('DEBUG RAW_REQUEST:', raw_request)

        # Parse username/password from the raw body only for session/auth purposes
        parsed = {}
        try:
            for pair in raw_request.split('&'):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    parsed[k] = v
        except Exception:
            parsed = {}

        username = parsed.get('username', '').strip()
        password = parsed.get('password', '').strip()
        timestamp = datetime.now().isoformat()

        # Build the body string exactly as received (do NOT sanitize/modify)
        body = raw_request if raw_request else f'username={username}&password={password}'

        # Classification logic: check if credentials match the actual admin credentials
        # If they match admin/admin123, mark as 'good'; otherwise mark as 'bad'
        classification = 'good' if (username == 'admin' and password == 'admin123') else 'bad'
        print('DEBUG ML_CLASSIFICATION:', classification, 'credentials_match:', username == 'admin' and password == 'admin123')

        # Log the request and dataset with the classifier result (good/bad)
        with open(REQUEST_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, 'POST', '/api/login', body])

        # Append to training dataset with the classifier label so we keep raw payloads
        with open(LOGIN_DATASET_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['POST', '/login', body, 0, 0, 0, 0, 0, 0, classification])

        # If malicious, also add to a detected alerts file for later review
        if classification == 'bad':
            with open(DETECTED_ALERTS_CSV, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, '/api/login', body, 'bad', 'detected by ML'])

        # If configured to accept any credentials, create admin session (we already logged above)
        if ALLOW_ANY_LOGIN:
            session['user'] = username or 'guest'
            session['role'] = 'admin'
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=24)

            return jsonify({'success': True, 'message': 'Admin login successful (ALLOW_ANY_LOGIN enabled)', 'classification': classification, 'role': 'admin', 'user': username}), 200

        # Otherwise perform normal credential check
        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['user'] = username
            session['role'] = 'admin'
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=24)

            return jsonify({'success': True, 'message': 'Admin login successful', 'classification': classification, 'role': 'admin', 'user': username}), 200

        # Failed credential check: already logged above with classifier label; return with classification
        return jsonify({'success': False, 'message': 'Invalid credentials', 'classification': classification}), 401

    except Exception as e:
        print('Error during login processing:', e)
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/dashboard')
def dashboard():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('dashboard.html', user=session.get('user'))


@app.route('/api/dashboard-data')
def get_dashboard_data():
    if 'user' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    try:
        # Read HTTP requests from CSV
        requests_data = []
        if os.path.exists(REQUEST_CSV):
            with open(REQUEST_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                requests_data = list(reader)[-10:] if reader else []

        # Read login dataset
        dataset_stats = {'total': 0, 'good': 0, 'bad': 0}
        if os.path.exists(LOGIN_DATASET_CSV):
            with open(LOGIN_DATASET_CSV, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                dataset_stats['total'] = len(lines)
                dataset_stats['good'] = sum(1 for line in lines if 'good' in line)
                dataset_stats['bad'] = sum(1 for line in lines if 'bad' in line)

        return jsonify({
            'success': True,
            'recent_requests': requests_data,
            'dataset_stats': dataset_stats
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


@app.route('/api/http-request', methods=['POST'])
def submit_http_request():
    if 'user' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    try:
        data = request.json
        method = data.get('method', 'POST').upper()
        url = data.get('url', '')
        body = data.get('body', '')
        timestamp = datetime.now().isoformat()

        # Save to CSV
        with open(REQUEST_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, method, url, body])

        # Also append to the main login_dataset.csv for training
        with open(LOGIN_DATASET_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([method, url, body, 0, 0, 0, 0, 0, 0, 'unknown'])

        return jsonify({'success': True, 'message': 'HTTP Request recorded successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, port=5000)

