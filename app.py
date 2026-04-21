from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
import re
import random

# =====================================
# APP CONFIG
# =====================================
app = Flask(__name__)

# Production CORS
CORS(
    app,
    resources={r"/*": {"origins": "*"}},   # Replace * with your frontend URL later
    supports_credentials=True
)

# =====================================
# LOAD MODEL
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "improved_fake_profile_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# =====================================
# CACHE
# =====================================
prediction_cache = {}

# =====================================
# HELPERS
# =====================================

def extract_username(input_text):
    if "instagram.com" in input_text:
        match = re.search(r"instagram\.com/([^/?]+)", input_text)
        if match:
            return match.group(1)
    return input_text.strip().lower()


def simulate_profile_data(username):
    random.seed(abs(hash(username)) % 100000)

    fake_like = random.random() < 0.4

    if fake_like:
        followers = random.randint(10, 80)
        following = random.randint(800, 2000)
        posts = random.randint(0, 5)
        bio_length = random.randint(0, 15)
        profile_pic = random.choice([0, 1])
        private = random.choice([0, 1])
    else:
        followers = random.randint(300, 5000)
        following = random.randint(100, 1500)
        posts = random.randint(20, 300)
        bio_length = random.randint(25, 150)
        profile_pic = 1
        private = 0

    external_url = 1 if random.random() > 0.7 else 0

    return {
        "profile pic": profile_pic,
        "#followers": followers,
        "#following": following,
        "#posts": posts,
        "description length": bio_length,
        "external URL": external_url,
        "private": private,
        "fullname": username.replace("_", " ").title(),
        "username": username
    }


def generate_features(profile):
    username = profile["username"]
    fullname = profile["fullname"]

    nums_length_username = sum(c.isdigit() for c in username) / max(len(username), 1)
    fullname_words = len(fullname.split())
    nums_length_fullname = sum(c.isdigit() for c in fullname) / max(len(fullname), 1)
    name_equals_username = 1 if username.lower() == fullname.lower() else 0

    engagement_ratio = profile["#followers"] / (profile["#following"] + 1)
    log_ratio = np.log1p(engagement_ratio)

    return [
        profile["profile pic"],
        nums_length_username,
        fullname_words,
        nums_length_fullname,
        name_equals_username,
        profile["description length"],
        profile["external URL"],
        profile["private"],
        profile["#posts"],
        profile["#followers"],
        profile["#following"],
        log_ratio
    ]


def explain_prediction(profile):
    reasons = []

    ratio = profile["#followers"] / (profile["#following"] + 1)

    if ratio < 0.1:
        reasons.append("Very low follower-following ratio")

    if profile["#posts"] < 5:
        reasons.append("Very few posts")

    if profile["profile pic"] == 0:
        reasons.append("No profile picture")

    if profile["description length"] < 10:
        reasons.append("Very short bio")

    if profile["external URL"] == 0:
        reasons.append("No external website")

    if profile["private"] == 1:
        reasons.append("Private account")

    if not reasons:
        reasons.append("Profile behaviour appears normal")

    return reasons


def get_risk_level(score):
    if score < 0.30:
        return "Low Risk"
    elif score < 0.70:
        return "Suspicious"
    return "High Risk"


# =====================================
# ROUTES
# =====================================

@app.route("/")
def home():
    return jsonify({
        "message": "AI Fake Profile Detection Backend Running 🚀",
        "status": "success"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "server": "running"
    })


# =====================================
# MANUAL PREDICTION
# =====================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        engagement_ratio = data["#followers"] / (data["#following"] + 1)
        log_ratio = np.log1p(engagement_ratio)

        features = [
            data["profile pic"],
            data["nums/length username"],
            data["fullname words"],
            data["nums/length fullname"],
            data["name==username"],
            data["description length"],
            data["external URL"],
            data["private"],
            data["#posts"],
            data["#followers"],
            data["#following"],
            log_ratio
        ]

        features = np.array(features).reshape(1, -1)
        features = scaler.transform(features)

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        return jsonify({
            "prediction": "Fake Profile" if prediction == 1 else "Genuine Profile",
            "risk_score": round(float(probability), 3),
            "risk_level": get_risk_level(float(probability)),
            "mode": "manual"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================
# AUTO ANALYZE
# =====================================
@app.route("/analyze-profile", methods=["POST"])
def analyze_profile():
    try:
        data = request.get_json()
        username = extract_username(data["input"])

        if username in prediction_cache:
            return jsonify(prediction_cache[username])

        profile = simulate_profile_data(username)

        features = generate_features(profile)
        features = np.array(features).reshape(1, -1)
        features = scaler.transform(features)

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        response = {
            "username": username,
            "prediction": "Fake Profile" if prediction == 1 else "Genuine Profile",
            "risk_score": round(float(probability), 3),
            "risk_level": get_risk_level(float(probability)),
            "mode": "auto",
            "reasons": explain_prediction(profile),
            "extracted_data": profile
        }

        prediction_cache[username] = response
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================
# MAIN
# =====================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)