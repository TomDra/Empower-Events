import React, { useState } from "react";
import axios from "axios";

// Define the Login component
const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Send a POST request to the server
    try {
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        email,
        password,
      });

      // Log success
      console.log('Login successful:', response.data);
    } catch (error) {
      // Log failure
      console.error('Login failed:', error.message);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="text"
            id="email"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;