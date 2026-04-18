from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS
import re
import random
import os

app = Flask(__name__)
CORS(app)

# ================= LOAD MODEL =================
model = joblib.load("model/improved_fake_profile_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# ================= CACHE =================
prediction_cache = {}

# ================= USERNAME EXTRACTION =================

def extract_username(input_text):

    if "instagram.com" in input_text:
        match = re.search(r"instagram\.com/([^/?]+)", input_text)

        if match:
            return match.group(1)

    return input_text.strip()


# ================= SIMULATED PROFILE =================

def simulate_profile_data(username):

    random.seed(hash(username) % 100000)

    fake_like = random.random() < 0.4

    if fake_like:

        followers = random.randint(10,80)
        following = random.randint(800,2000)
        posts = random.randint(0,5)
        bio_length = random.randint(0,15)
        profile_pic = random.choice([0,1])
        private = random.choice([0,1])

    else:

        followers = random.randint(300,5000)
        following = random.randint(100,1500)
        posts = random.randint(20,300)
        bio_length = random.randint(25,150)
        profile_pic = 1
        private = 0

    external_url = 1 if random.random() > 0.7 else 0

    return {

        "profile pic":profile_pic,
        "#followers":followers,
        "#following":following,
        "#posts":posts,
        "description length":bio_length,
        "external URL":external_url,
        "private":private,
        "fullname":username.replace("_"," ").title(),
        "username":username

    }


# ================= FEATURE GENERATION =================

def generate_features(profile_data):

    username = profile_data["username"]
    fullname = profile_data["fullname"]

    nums_length_username = sum(c.isdigit() for c in username)/len(username)

    fullname_words = len(fullname.split())

    nums_length_fullname = sum(c.isdigit() for c in fullname)/len(fullname)

    name_equals_username = 1 if username.lower()==fullname.lower() else 0

    engagement_ratio = profile_data["#followers"]/(profile_data["#following"]+1)

    log_engagement_ratio = np.log1p(engagement_ratio)

    return [

        profile_data["profile pic"],
        nums_length_username,
        fullname_words,
        nums_length_fullname,
        name_equals_username,
        profile_data["description length"],
        profile_data["external URL"],
        profile_data["private"],
        profile_data["#posts"],
        profile_data["#followers"],
        profile_data["#following"],
        log_engagement_ratio

    ]


# ================= EXPLAINABLE AI =================

def explain_prediction(profile_data):

    reasons = []

    followers = profile_data["#followers"]
    following = profile_data["#following"]
    posts = profile_data["#posts"]
    bio_length = profile_data["description length"]

    ratio = followers/(following+1)

    if ratio < 0.1:
        reasons.append("Very low follower-following ratio")

    if posts < 5:
        reasons.append("Very few posts")

    if profile_data["profile pic"] == 0:
        reasons.append("No profile picture")

    if bio_length < 10:
        reasons.append("Very short bio")

    if profile_data["external URL"] == 0:
        reasons.append("No external website")

    if profile_data["private"] == 1:
        reasons.append("Private account")

    if len(reasons)==0:
        reasons.append("Profile behaviour appears normal")

    return reasons


# ================= RISK LEVEL =================

def get_risk_level(score):

    if score < 0.3:
        return "Low Risk"

    elif score < 0.7:
        return "Suspicious"

    else:
        return "High Risk"


# ================= ROUTES =================

@app.route("/")
def home():
    return "Fake Profile Detection API running"


# ---------- MANUAL MODE ----------

@app.route("/predict",methods=["POST"])
def predict():

    try:

        data = request.get_json()

        engagement_ratio = data["#followers"]/(data["#following"]+1)

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

        features = np.array(features).reshape(1,-1)

        features = scaler.transform(features)

        prediction = model.predict(features)[0]

        probability = model.predict_proba(features)[0][1]

        risk_score = round(float(probability),3)

        risk_level = get_risk_level(risk_score)

        result = "Fake Profile" if prediction==1 else "Genuine Profile"

        return jsonify({

            "prediction":result,
            "risk_score":risk_score,
            "risk_level":risk_level,
            "mode":"manual"

        })

    except Exception as e:

        return jsonify({"error":str(e)})


# ---------- AUTO MODE ----------

@app.route("/analyze-profile",methods=["POST"])
def analyze_profile():

    try:

        data = request.get_json()

        username = extract_username(data["input"])

        if username in prediction_cache:

            return jsonify(prediction_cache[username])

        profile_data = simulate_profile_data(username)

        features = generate_features(profile_data)

        features = np.array(features).reshape(1,-1)

        features = scaler.transform(features)

        prediction = model.predict(features)[0]

        probability = model.predict_proba(features)[0][1]

        risk_score = round(float(probability),3)

        risk_level = get_risk_level(risk_score)

        result = "Fake Profile" if prediction==1 else "Genuine Profile"

        reasons = explain_prediction(profile_data)

        response = {

            "username":username,
            "prediction":result,
            "risk_score":risk_score,
            "risk_level":risk_level,
            "mode":"auto",
            "reasons":reasons,
            "extracted_data":profile_data

        }

        prediction_cache[username] = response

        return jsonify(response)

    except Exception as e:

        return jsonify({"error":str(e)})



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)