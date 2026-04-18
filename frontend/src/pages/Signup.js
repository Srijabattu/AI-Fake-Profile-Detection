import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createUserWithEmailAndPassword, signOut } from "firebase/auth";
import { auth } from "../firebase";
import "../App.css";

function Signup() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      await createUserWithEmailAndPassword(auth, email, password);

      // 🔥 Force logout after signup
      await signOut(auth);

      alert("Account created! Please login.");
      navigate("/");

    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="container">
      <div className="cardWrapper">

        <h2 className="title">Signup</h2>

        <div className="formGroup">
          <input
            placeholder="Email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />
        </div>

        <div className="formGroup">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />
        </div>

        <div className="buttonGroup">
          <button onClick={handleSignup}>Signup</button>
        </div>

        <p className="smallText" onClick={()=>navigate("/")}>
          Go to Login
        </p>

      </div>
    </div>
  );
}

export default Signup;