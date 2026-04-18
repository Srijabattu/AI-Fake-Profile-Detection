import React, { useState } from "react";
import "../App.css";
import RiskMeter from "../components/RiskMeter";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";

function Dashboard() {

  const [mode, setMode] = useState("auto");
  const [username, setUsername] = useState("");

  const [manualData, setManualData] = useState({
    "profile pic": 1,
    "nums/length username": 0,
    "fullname words": 2,
    "nums/length fullname": 0,
    "name==username": 0,
    "description length": 20,
    "external URL": 0,
    "private": 0,
    "#posts": 10,
    "#followers": 500,
    "#following": 200
  });

  const [result, setResult] = useState(null);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);

  const handleChange = (e) => {
    setManualData({
      ...manualData,
      [e.target.name]: Number(e.target.value)
    });
  };

  const handleLogout = async () => {
    await signOut(auth);
    window.location.href = "/";
  };

  const analyzeAuto = async () => {
  if (!username) {
    alert("Please enter username");
    return;
  }

  try {
    const res = await fetch("https://ai-fake-profile-detection-gtla.onrender.com/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ input: username })
    });

    const data = await res.json();
    console.log(data);

    setResult(data);
    setHasAnalyzed(true);

  } catch (error) {
    console.log(error);
    alert(error.message);
  }
};
  const analyzeManual = async () => {
    try {
      const res = await fetch("https://ai-fake-profile-detection-gtla.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(manualData)
      });

      const data = await res.json();
      setResult(data);
      setHasAnalyzed(true);

    } catch {
      alert("Backend connection failed");
    }
  };

  return (
    <div className="container">
      <div className="cardWrapper">

        <button onClick={handleLogout} style={{float:"right", width:"auto"}}>
          Logout
        </button>

        <h2 className="title">AI Profile Detector</h2>

        <div className="modeButtons">
          <button onClick={() => {
            setMode("auto");
            setResult(null);
            setHasAnalyzed(false);
          }}>Auto</button>

          <button onClick={() => {
            setMode("manual");
            setResult(null);
            setHasAnalyzed(false);
          }}>Manual</button>
        </div>

        {/* AUTO MODE */}
        {mode === "auto" && (
  <>
    <p className="title">Analyze Profile</p>

    <div className="formGroup">
      <input
        type="text"
        placeholder="Enter username or URL"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
    </div>

    <button onClick={analyzeAuto}>Analyze</button>
  </>
)}

        {/* MANUAL MODE (GRID) */}
        {mode === "manual" && (
          <>
            <p className="title">Manual Input</p>

            <div className="gridForm">

              <input name="profile pic" placeholder="Profile Pic" onChange={handleChange}/>
              <input name="nums/length username" placeholder="Username Ratio" onChange={handleChange}/>
              <input name="fullname words" placeholder="Fullname Words" onChange={handleChange}/>

              <input name="nums/length fullname" placeholder="Fullname Ratio" onChange={handleChange}/>
              <input name="name==username" placeholder="Name Match" onChange={handleChange}/>
              <input name="description length" placeholder="Bio Length" onChange={handleChange}/>

              <input name="external URL" placeholder="External URL" onChange={handleChange}/>
              <input name="private" placeholder="Private" onChange={handleChange}/>
              <input name="#posts" placeholder="Posts" onChange={handleChange}/>

              <input name="#followers" placeholder="Followers" onChange={handleChange}/>
              <input name="#following" placeholder="Following" onChange={handleChange}/>

            </div>

            <button onClick={analyzeManual}>Analyze</button>
          </>
        )}

        {/* RESULT ONLY AFTER ANALYZE */}
        {hasAnalyzed && result && (
          <div className="result">

            <h3>Result</h3>

            <p><b>{result.prediction}</b></p>

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

            {result.reasons && (
              <>
                <h4>Why?</h4>
                <ul>
                  {result.reasons.map((r, i) => (
                    <li key={i}>{r}</li>
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