import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import os

# Create model folder if it doesn't exist
os.makedirs("model", exist_ok=True)

print("Loading datasets...")

# ================= LOAD DATA =================
train_data = pd.read_csv("dataset/insta_train.csv")
test_data = pd.read_csv("dataset/insta_test.csv")

print("Train Shape:", train_data.shape)
print("Test Shape:", test_data.shape)

# ================= ADD ENGAGEMENT RATIO =================
for df in [train_data, test_data]:
    df["engagement_ratio"] = df["#followers"] / (df["#follows"] + 1)

# ================= FEATURES =================
feature_columns = [
    'profile pic',
    'nums/length username',
    'fullname words',
    'nums/length fullname',
    'name==username',
    'description length',
    'external URL',
    'private',
    '#posts',
    '#followers',
    '#follows',
    'engagement_ratio'
]

X_train = train_data[feature_columns]
y_train = train_data["fake"]

X_test = test_data[feature_columns]
y_test = test_data["fake"]

# ================= SCALING =================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training improved Random Forest model...")

# ================= MODEL =================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42
)

model.fit(X_train_scaled, y_train)

print("Making predictions...")

y_pred = model.predict(X_test_scaled)

# ================= EVALUATION =================
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ================= SAVE =================
joblib.dump(model, "model/improved_fake_profile_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Improved model saved successfully inside model folder!")

print("\nImproved model saved successfully!")