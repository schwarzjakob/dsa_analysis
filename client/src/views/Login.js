import React from "react";
import "../App.css"; // Assuming you have a separate CSS file for styling

function Login() {
  const initiateLogin = async () => {
    try {
      window.location.href = "http://127.0.0.1:5000/auth/login";
    } catch (error) {
      console.error("Login error", error);
    }
  };

  return (
    <div className="login-container">
      <header className="login-header">
        <h1>Welcome to the DSA Dashboard</h1>
        <p>Explore and analyze your adventure data</p>
      </header>
      <div className="login-form">
        <button onClick={initiateLogin} className="login-button">
          Login with Google
        </button>
        {/* Future space for standard login form */}
      </div>
    </div>
  );
}

export default Login;
