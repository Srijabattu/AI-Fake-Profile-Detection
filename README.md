# AI-Based Fake Profile & Scam Detection System

An intelligent web application designed to detect fake social media profiles and scam-related behavior using **Machine Learning**, **Natural Language Processing**, and a modern **Full-Stack Web Architecture**.

This project helps improve online safety by analyzing profile details, activity patterns, and suspicious indicators to classify whether a profile is **Genuine** or **Fake/Scam**.

---

## 🚀 Features

* 🔍 Detect fake social media profiles instantly
* 🤖 Machine Learning based prediction system
* 📊 Scam risk score generation
* 📱 Modern responsive frontend UI
* 🔐 Firebase Authentication (Login / Signup)
* 🌐 Full-stack deployment support
* ⚡ Real-time profile analysis
* 📈 Easy-to-understand prediction results

---

## 🛠️ Tech Stack

### Frontend

* React.js
* HTML5
* CSS3
* JavaScript
* Tailwind CSS (if used)

### Backend

* Flask (Python)

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Database / Authentication

* Firebase Authentication
* Firestore Database

### Deployment

* Vercel (Frontend)
* Render (Backend)

---

## 📂 Project Structure

```bash
AI-Fake-Profile-Detection/
│── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
│── backend/
│   ├── app.py
│   ├── model.pkl
│   ├── requirements.txt
│   └── utils/
│
│── README.md
```

---

## ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Fake-Profile-Detection.git
cd AI-Fake-Profile-Detection
```

---

## 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

---

## 3️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs on:

```bash
http://localhost:5000
```

---

## 🔐 Environment Variables

Create `.env` file inside frontend:

```env
REACT_APP_FIREBASE_API_KEY=your_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_domain
REACT_APP_FIREBASE_PROJECT_ID=your_id
```

Backend `.env`

```env
MODEL_PATH=model.pkl
```

---

## 🤖 How It Works

1. User enters profile details
2. Frontend sends data to Flask API
3. ML model analyzes suspicious patterns
4. System predicts:

* Genuine Profile ✅
* Fake Profile ❌
* Scam Risk ⚠️

5. Result displayed with score

---

## 📊 ML Model Inputs

Examples of features used:

* Number of followers
* Following ratio
* Username length
* Bio presence
* Profile image existence
* Post count
* Account age
* Suspicious keywords
* Engagement anomalies

---

## 📸 Screenshots

Add your screenshots here:

```bash
/screenshots/home.png
/screenshots/result.png
/screenshots/login.png
```

---

## 🌍 Deployment Links

### Frontend:

```bash
https://your-frontend.vercel.app
```

### Backend:

```bash
https://your-backend.onrender.com
```

---

## 🔧 Future Enhancements

* Deep Learning model integration
* Real-time Instagram / X profile scanner
* Browser extension support
* Explainable AI dashboard
* Fraud network detection
* Mobile App version

---

## 👨‍💻 Author

**Srija Battu**
B.Tech Final Year Project

---

## 📜 License

This project is developed for academic and educational purposes.

---

## ⭐ Support

If you like this project:

* Star ⭐ the repository
* Fork 🍴 the project
* Contribute 💡 improvements

---
