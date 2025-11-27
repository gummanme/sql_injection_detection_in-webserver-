import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
df = pd.read_csv('login_dataset.csv', header=None)
df.columns = ['method', 'endpoint', 'body', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'label']

# Display dataset info
print(f"Dataset shape: {df.shape}")
print(f"Label distribution:\n{df['label'].value_counts()}")

# Feature engineering
# We'll create features from the body (login credentials)
def extract_features(body):
    features = {
        'body_length': len(str(body)),
        'has_special_chars': 1 if any(c in str(body) for c in ["'", '"', '-', ';', '*']) else 0,
        'has_sql_keywords': 1 if any(kw in str(body).lower() for kw in ['union', 'select', 'drop', 'insert', 'update', 'delete', 'exec', 'script']) else 0,
        'has_path_traversal': 1 if '..' in str(body) else 0,
        'body_contains_slash': str(body).count('/'),
    }
    return features

# Extract features for each row
feature_list = []
for idx, row in df.iterrows():
    features = extract_features(row['body'])
    features['f1'] = row['f1']
    features['f2'] = row['f2']
    features['f3'] = row['f3']
    feature_list.append(features)

features_df = pd.DataFrame(feature_list)

# Prepare X and y
X = features_df
y = (df['label'] == 'bad').astype(int)  # 1 for bad, 0 for good

print(f"\nFeatures shape: {X.shape}")
print(f"Target distribution:\n{y.value_counts()}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("\nTraining model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"\nTrain Accuracy: {train_score:.4f}")
print(f"Test Accuracy: {test_score:.4f}")

# Save model and feature list
joblib.dump(model, 'login_classifier.pkl')
joblib.dump(features_df.columns.tolist(), 'feature_columns.pkl')
print("\nModel saved as 'login_classifier.pkl'")
print("Feature columns saved as 'feature_columns.pkl'")
