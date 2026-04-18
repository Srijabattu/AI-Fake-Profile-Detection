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

# Global CORS
CORS(app)

# =====================================
# LOAD MODEL
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(BASE_DIR, "model/improved_fake_profile_model.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "model/scaler.pkl")
)

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

    return input_text.strip()


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
    username = profile.get("username", "")
    fullname = profile.get("fullname", "")

    followers = profile.get("#followers", 0)
    following = profile.get("#following", 1)
    posts = profile.get("#posts", 0)

    nums_length_username = sum(c.isdigit() for c in username) / max(len(username), 1)
    nums_length_fullname = sum(c.isdigit() for c in fullname) / max(len(fullname), 1)

    fullname_words = len(fullname.split())

    name_equals_username = 1 if username.lower() == fullname.lower() else 0

    engagement_ratio = followers / (following + 1)
    log_ratio = np.log1p(engagement_ratio)

    return [
        profile.get("profile pic", 0),
        nums_length_username,
        fullname_words,
        nums_length_fullname,
        name_equals_username,
        profile.get("description length", 0),
        profile.get("external URL", 0),
        profile.get("private", 0),
        posts,
        followers,
        following,
        log_ratio
    ]


def explain_prediction(profile):
    reasons = []

    followers = profile.get("#followers", 0)
    following = profile.get("#following", 1)
    posts = profile.get("#posts", 0)
    bio = profile.get("description length", 0)

    ratio = followers / (following + 1)

    if ratio < 0.1:
        reasons.append("Very low follower-following ratio")

    if posts < 5:
        reasons.append("Very few posts")

    if profile.get("profile pic", 0) == 0:
        reasons.append("No profile picture")

    if bio < 10:
        reasons.append("Very short bio")

    if profile.get("external URL", 0) == 0:
        reasons.append("No external website")

    if profile.get("private", 0) == 1:
        reasons.append("Private account")

    if not reasons:
        reasons.append("Profile behaviour appears normal")

    return reasons


def get_risk_level(score):
    if score < 0.3:
        return "Low Risk"
    elif score < 0.7:
        return "Suspicious"
    return "High Risk"


# =====================================
# FORCE HEADERS
# =====================================
@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# =====================================
# HOME
# =====================================
@app.route("/")
def home():
    return "<h1>Backend Running Successfully 🚀</h1>"


# =====================================
# MANUAL MODE
# =====================================
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():

    if request.method == "OPTIONS":
        return jsonify({"message": "preflight ok"}), 200

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

        result = "Fake Profile" if prediction == 1 else "Genuine Profile"

        return jsonify({
            "prediction": result,
            "risk_score": round(float(probability), 3),
            "risk_level": get_risk_level(float(probability)),
            "mode": "manual"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================
# AUTO MODE
# =====================================
@app.route("/analyze-profile", methods=["GET", "POST", "OPTIONS"])
def analyze_profile():

    if request.method == "GET":
        return "Use POST request for analyze-profile API"

    if request.method == "OPTIONS":
        return jsonify({"message": "preflight ok"}), 200

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

        result = "Fake Profile" if prediction == 1 else "Genuine Profile"

        response = {
            "username": username,
            "prediction": result,
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
# RUN
# =====================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)