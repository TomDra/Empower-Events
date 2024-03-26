import React, { useState } from "react";
import axios from "axios";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

//TODO: Change username and password to email and password
// Define the Login component
const Login = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  // function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Send a POST request to the server
    try {
      const response = await axios.post('http://localhost:3000/api/auth/login/', { // miles why did you write 8000 wasted 9 hours of my life
        //TODO: Change username and password to email and password
        username: username,
        password: password,
      });

      // Log success
      console.log('Login successful:', response.data);
      setCurrentUser(true);
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
          <label htmlFor="email">Username:</label>
          <input
            type="text"
            id="email"
            onChange={(e) => setUsername(e.target.value)}
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