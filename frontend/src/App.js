import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";

import { auth } from "./firebase";
import { onAuthStateChanged } from "firebase/auth";

function App() {

  const [user, setUser] = useState(undefined);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  if (user === undefined) return <div>Loading...</div>;

  return (
    <BrowserRouter>
      <Routes>

        {/* Login */}
        <Route path="/" element={user ? <Dashboard /> : <Login />} />

        {/* Signup */}
        <Route path="/signup" element={<Signup />} />

        {/* Dashboard (Protected) */}
        <Route path="/dashboard" element={user ? <Dashboard /> : <Login />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;