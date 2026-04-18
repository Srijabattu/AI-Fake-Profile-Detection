import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier

from feature_utils import *

print("Loading dataset...")

data = pd.read_csv("dataset/insta_train.csv")

# Feature engineering
data["digit_ratio"] = data["username"].apply(digit_ratio)
data["underscore_count"] = data["username"].apply(underscore_count)
data["username_length"] = data["username"].apply(username_length)
data["username_entropy"] = data["username"].apply(username_entropy)

data["engagement_ratio"] = data["#followers"] / (data["#follows"] + 1)

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

'digit_ratio',
'underscore_count',
'username_length',
'username_entropy',
'engagement_ratio'
]

X = data[feature_columns]
y = data["fake"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Base models
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

gb = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05
)

# Stacking model
model = StackingClassifier(
    estimators=[
        ('rf', rf),
        ('gb', gb)
    ],
    final_estimator=LogisticRegression()
)

print("Training Model V3...")

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, pred))
print("\nClassification Report:\n", classification_report(y_test, pred))

joblib.dump(model, "model/fake_profile_model_v3.pkl")
joblib.dump(scaler, "model/scaler_v3.pkl")

print("\nModel V3 saved successfully!")