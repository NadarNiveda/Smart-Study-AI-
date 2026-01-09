import { useState } from "react";

function Signup({ goToLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = () => {
    if (name && email && password) {
      alert("Signup successful! Please login.");
      goToLogin();
    }
  };

  return (
    <div className="auth-container">
      <h2>Create Smart-Study Account</h2>

      <input
        placeholder="Full Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />

      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      <button onClick={handleSignup}>Sign Up</button>

      <p>
        Already have an account?{" "}
        <span onClick={goToLogin}>Login</span>
      </p>
    </div>
  );
}

export default Signup;
