import React, { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";

import { auth } from "./firebase";
import { onAuthStateChanged } from "firebase/auth";

function App() {
  const [user, setUser] = useState(undefined);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser || null);
    });

    return () => unsubscribe();
  }, []);

  if (user === undefined) {
    return <div style={{ padding: "40px" }}>Loading...</div>;
  }

  return (
    <BrowserRouter>
      <Routes>

        {/* Home/Login */}
        <Route
          path="/"
          element={
            user ? <Navigate to="/dashboard" /> : <Login />
          }
        />

        {/* Signup */}
        <Route
          path="/signup"
          element={
            user ? <Navigate to="/dashboard" /> : <Signup />
          }
        />

        {/* Protected Dashboard */}
        <Route
          path="/dashboard"
          element={
            user ? <Dashboard /> : <Navigate to="/" />
          }
        />

        {/* Unknown Routes */}
        <Route
          path="*"
          element={<Navigate to="/" />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;