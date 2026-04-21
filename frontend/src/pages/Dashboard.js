import React, { useState } from "react";
import "../App.css";
import RiskMeter from "../components/RiskMeter";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";

function Dashboard() {
  const [mode, setMode] = useState("auto");
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);

  const [manualData, setManualData] = useState({
    "profile pic": 1,
    "nums/length username": 0,
    "fullname words": 2,
    "nums/length fullname": 0,
    "name==username": 0,
    "description length": 20,
    "external URL": 0,
    private: 0,
    "#posts": 10,
    "#followers": 500,
    "#following": 200
  });

  const [result, setResult] = useState(null);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);

  // ✅ LIVE RAILWAY BACKEND
  const BACKEND_URL = "https://web-production-9effe.up.railway.app";

  const handleChange = (e) => {
    setManualData({
      ...manualData,
      [e.target.name]: Number(e.target.value)
    });
  };

  const resetResult = () => {
    setResult(null);
    setHasAnalyzed(false);
  };

  const handleLogout = async () => {
    await signOut(auth);
    window.location.href = "/";
  };

  // ================= AUTO MODE =================
  const analyzeAuto = async () => {
    if (!username.trim()) {
      alert("Please enter username or Instagram URL");
      return;
    }

    try {
      setLoading(true);
      resetResult();

      const res = await fetch(`${BACKEND_URL}/analyze-profile`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          input: username
        })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Analysis failed");
      }

      setResult(data);
      setHasAnalyzed(true);
    } catch (error) {
      console.log(error);
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  // ================= MANUAL MODE =================
  const analyzeManual = async () => {
    try {
      setLoading(true);
      resetResult();

      const res = await fetch(`${BACKEND_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(manualData)
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Prediction failed");
      }

      setResult(data);
      setHasAnalyzed(true);
    } catch (error) {
      console.log(error);
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="cardWrapper">
        <button
          onClick={handleLogout}
          style={{ float: "right", width: "auto" }}
        >
          Logout
        </button>

        <h2 className="title">AI Fake Profile Detector</h2>

        {/* MODE BUTTONS */}
        <div className="modeButtons">
          <button
            onClick={() => {
              setMode("auto");
              resetResult();
            }}
          >
            Auto
          </button>

          <button
            onClick={() => {
              setMode("manual");
              resetResult();
            }}
          >
            Manual
          </button>
        </div>

        {/* ================= AUTO MODE ================= */}
        {mode === "auto" && (
          <>
            <p className="title">Analyze Profile</p>

            <div className="formGroup">
              <input
                type="text"
                placeholder="Enter username or Instagram URL"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <button onClick={analyzeAuto} disabled={loading}>
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </>
        )}

        {/* ================= MANUAL MODE ================= */}
        {mode === "manual" && (
          <>
            <p className="title">Manual Input</p>

            <div className="gridForm">
              <input
                name="profile pic"
                placeholder="Profile Pic (0/1)"
                onChange={handleChange}
              />

              <input
                name="nums/length username"
                placeholder="Username Ratio"
                onChange={handleChange}
              />

              <input
                name="fullname words"
                placeholder="Fullname Words"
                onChange={handleChange}
              />

              <input
                name="nums/length fullname"
                placeholder="Fullname Ratio"
                onChange={handleChange}
              />

              <input
                name="name==username"
                placeholder="Name Match (0/1)"
                onChange={handleChange}
              />

              <input
                name="description length"
                placeholder="Bio Length"
                onChange={handleChange}
              />

              <input
                name="external URL"
                placeholder="External URL (0/1)"
                onChange={handleChange}
              />

              <input
                name="private"
                placeholder="Private (0/1)"
                onChange={handleChange}
              />

              <input
                name="#posts"
                placeholder="Posts"
                onChange={handleChange}
              />

              <input
                name="#followers"
                placeholder="Followers"
                onChange={handleChange}
              />

              <input
                name="#following"
                placeholder="Following"
                onChange={handleChange}
              />
            </div>

            <button onClick={analyzeManual} disabled={loading}>
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </>
        )}

        {/* ================= RESULT ================= */}
        {hasAnalyzed && result && (
          <div className="result">
            <h3>Result</h3>

            <p>
              <b>{result.prediction}</b>
            </p>

            <p>
              <b>Risk:</b>{" "}
              <span
                className={
                  result.risk_level === "Low Risk"
                    ? "lowRisk"
                    : result.risk_level === "Suspicious"
                    ? "midRisk"
                    : "highRisk"
                }
              >
                {result.risk_level}
              </span>
            </p>

            <RiskMeter score={result.risk_score} />

            {/* AUTO MODE REASONS */}
            {result.reasons && (
              <>
                <h4>Why?</h4>
                <ul>
                  {result.reasons.map((reason, index) => (
                    <li key={index}>{reason}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;