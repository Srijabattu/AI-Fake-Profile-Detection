import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut
} from "firebase/auth";
import { auth, provider } from "../firebase";
import "../App.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      window.location.href = "/dashboard";
    } catch (err) {
      alert(err.message);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);

      const confirmUser = window.confirm(
        `Continue as ${result.user.email}?`
      );

      if (!confirmUser) {
        await signOut(auth);
        return;
      }

      // wait tiny moment for auth sync
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 500);

    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="container">
      <div className="cardWrapper">

        <h2 className="title">Login</h2>

        <div className="formGroup">
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="formGroup">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="buttonGroup">
          <button onClick={handleLogin}>Login</button>

          <button onClick={handleGoogleLogin}>
            Google Login
          </button>
        </div>

        <p
          className="smallText"
          onClick={() => navigate("/signup")}
        >
          Create Account
        </p>

      </div>
    </div>
  );
}

export default Login;