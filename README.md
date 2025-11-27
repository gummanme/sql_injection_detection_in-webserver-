# 🔐 Login Security Classifier System

A complete machine learning-based login security system with a beautiful company login website and Streamlit classification interface.

## 📋 Project Structure

```
csvmy/
├── venv/                          # Virtual environment
├── login_dataset.csv             # Training/test dataset
├── login_credentials.csv         # Saved login credentials
├── login_classifier.pkl          # Trained ML model
├── feature_columns.pkl           # Feature column names
├── generated_login_dataset.py    # Dataset generation script
├── train_model.py                # Model training script
├── app.py                        # Flask web app (company login website)
├── app_streamlit.py             # Streamlit classification app
├── templates/
│   └── index.html               # Company login page HTML
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Navigate to project folder
cd d:\csvmy

# Virtual environment is already created
# Activate it
.\venv\Scripts\activate
```

### 2. Install Dependencies

All required packages are already installed:

- pandas
- numpy
- scikit-learn
- streamlit
- flask
- joblib

### 3. Generate Dataset

The dataset has already been generated! To regenerate:

```bash
.\venv\Scripts\python generated_login_dataset.py
```

### 4. Train Model

The model has already been trained! To retrain:

```bash
.\venv\Scripts\python train_model.py
```

Output:

```
Dataset shape: (1000, 10)
Train Accuracy: 100.00%
Test Accuracy: 100.00%
```

## 🌐 Running the Applications

### Option 1: Company Login Website (Flask)

```bash
cd d:\csvmy
.\venv\Scripts\python app.py
```

Access at: `http://localhost:5000`

Features:

- Professional company login interface
- Beautiful gradient UI design
- Saves login credentials to `login_credentials.csv`
- Appends new credentials to training dataset

### Option 2: Streamlit Classification App

```bash
cd d:\csvmy
.\venv\Scripts\streamlit run app_streamlit.py
```

Features:

- 🔍 **Classify Credentials**: Check if credentials are malicious
- 📜 **View History**: See all saved credentials
- 📊 **Statistics**: Model performance and dataset analysis
- ℹ️ **About**: Information about the classifier

## 🤖 How the Classifier Works

### Features Analyzed

1. **Body Length** - Length of the credential string
2. **Special Characters** - Presence of SQL/injection chars ('`, ", -, ;, \*)
3. **SQL Keywords** - Detection of UNION, SELECT, DROP, INSERT, UPDATE, DELETE, EXEC, SCRIPT
4. **Path Traversal** - Detection of `..` patterns
5. **Slashes** - Count of forward slashes (/)

### Model Details

- **Algorithm**: Random Forest Classifier
- **Training Samples**: 1000 (500 good, 500 bad)
- **Training Accuracy**: 100%
- **Test Accuracy**: 100%

### Classification Output

- **Legitimate (Good)**: Standard login attempts
- **Suspicious (Bad)**: SQL injection, XSS, path traversal attempts

## 📊 Dataset

The training dataset contains:

- **500 Legitimate Logins**: Random usernames and passwords
- **500 Malicious Attempts**: SQL injection, XSS, path traversal payloads

Sample payloads detected:

```
admin' OR '1'='1
' UNION SELECT * FROM users --
'; DROP TABLE users;--
<script>alert(1)</script>
../../etc/passwd
```

## 💾 Data Storage

### login_credentials.csv

Stores all credentials submitted through the Streamlit app:

```csv
timestamp,username,password
2025-11-27T23:45:00,user@example.com,password123
```

### login_dataset.csv

Appends new classifications:

```csv
POST,/login,username=user&password=pass,0,0,0,0,0,0,good
POST,/login,username=admin' OR '1'='1,0,0,0,0,0,0,bad
```

## 🔒 Security Features

1. ✅ **Local Processing** - All data processed locally
2. ✅ **Feature Analysis** - Pattern-based detection
3. ✅ **Confidence Scores** - Probability-based classification
4. ✅ **Real-time Updates** - Model updates with new data

## 📈 Model Performance

```
Training Accuracy: 100%
Testing Accuracy: 100%
Precision: 100%
Recall: 100%
```

## 🔧 Technical Stack

- **Backend**: Flask (Web server), Python (ML)
- **Frontend**: HTML/CSS (Beautiful UI)
- **ML Framework**: Scikit-learn (Random Forest)
- **Interactive UI**: Streamlit
- **Data Processing**: Pandas, NumPy

## 📝 Usage Examples

### Example 1: Legitimate Login

```
Input: username="john@company.com", password="SecurePass123"
Output: ✅ LEGITIMATE LOGIN (Confidence: 100%)
```

### Example 2: SQL Injection

```
Input: username="admin' OR '1'='1", password="anything"
Output: ⚠️ SUSPICIOUS LOGIN (Confidence: 100%)
```

### Example 3: XSS Attempt

```
Input: username="<script>alert(1)</script>", password="test"
Output: ⚠️ SUSPICIOUS LOGIN (Confidence: 100%)
```

## 🎨 Company Website Features

- Modern gradient design (Purple/Blue theme)
- Responsive layout (Desktop & Mobile)
- Professional branding
- Security features highlight:
  - 256-bit SSL Encryption
  - Two-Factor Authentication
  - Real-time Activity Monitoring
  - GDPR Compliant

## 📚 Files Included

1. **generated_login_dataset.py** - Dataset generation (1000 records)
2. **train_model.py** - Model training script
3. **app.py** - Flask web application
4. **app_streamlit.py** - Streamlit classification interface
5. **templates/index.html** - Company login website
6. **login_dataset.csv** - Training dataset
7. **login_classifier.pkl** - Trained model
8. **feature_columns.pkl** - Feature names

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is in use:

```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F
```

### Model Not Found

Run training first:

```bash
.\venv\Scripts\python train_model.py
```

### Permission Denied

Run PowerShell as Administrator or adjust execution policy:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📧 Support

For issues or questions, check the About section in the Streamlit app.

## ⚖️ License

This project is for educational purposes only.

---

**Created with ❤️ for security-conscious developers**
