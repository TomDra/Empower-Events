import React, { useEffect, useState } from "react";
// Importing necessary modules and components from React and Material-UI

import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Typography, Container, Box } from "@mui/material";

// Setting Axios defaults for CSRF protection and enabling credentials
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;


// Defining the Login component
const Login = () => {

  // Initializing state variables using the useState hook
  const [currentUser, setCurrentUser] = useState(null); // To track the current user
  const [username, setUsername] = useState(""); // To store the entered username
  const [password, setPassword] = useState(""); // To store the entered password
  const navigate = useNavigate();

  // Handling form submission
  const handleSubmit = async (e) => {
    
    // Send a POST request to the server
    e.preventDefault(); // Preventing default form submission behavior
    try {
      // Sending a POST request to the backend API for login
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        username, // Sending username entered by the user
        password, // Sending password entered by the user
      });
      // Log success
      console.log('Login successful:', response.data); // Logging successful login response
      setCurrentUser(true); // Setting currentUser to true upon successful login
      // Redirect to the home page
      navigate("/");
    } catch (error) {
      // Log failure
      console.error('Login failed:', error.message); // Logging error message if login fails
      alert("Login failed. Please try again.");
    }
  };

  // Rendering the login form
  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          {/* Username input field */}
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={(e) => setUsername(e.target.value)} // Handling username input change
          />
          {/* Password input field */}
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Handling password input change
          />
          {/* Submit button */}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign In
          </Button>
        </Box>
        <a href="/register">Sign Up instead</a>
      </Box>
    </Container>
  );
};


// Exporting the Login component as the default export
export default Login;
