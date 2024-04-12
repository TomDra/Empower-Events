import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

//TODO: Change username and password to email and password
// Define the Login component
const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Send a POST request to the server
    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        {
          //TODO: Change username and password to email and password
          username: username,
          password: password,
        }
      );

      // Log success
      console.log("Login successful:", response.data);
      // Redirect to the home page
      navigate("/");
    } catch (error) {
      // Log failure
      console.error("Login failed:", error.message);
      alert("Login failed. Please try again.");
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <form onSubmit={(e) => handleSubmit(e)}>
                <h1>Login</h1>
                <div className="form-group mt-3">
                  <label>Username</label>
                  <input
                    type="username"
                    className="form-control mt-1"
                    placeholder="Enter username"
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group mt-3 mb-2">
                  <label>Password</label>
                  <input
                    type="password"
                    className="form-control mt-1"
                    placeholder="Enter password"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <a href="/signup">Sign Up instead</a>
                <div className="form-group mt-2"></div>
                <div className="d-grid gap-2 mt-3">
                  <button type="submit" className="btn btn-primary">
                    Log In
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
