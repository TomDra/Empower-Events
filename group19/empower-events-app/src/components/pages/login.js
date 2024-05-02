import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Typography, Container, Box } from "@mui/material";
import { speak } from "../../utils/CheckSpeech"; // Adjust the path based on your actual file structure

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

const Login = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSpeak = () => {
    // Reading out the welcome message and input field descriptions
    speak("Welcome to the login page. Please enter your username and password to sign in.");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        username,
        password,
      });
      console.log('Login successful:', response.data);
      setCurrentUser(true);
      navigate("/");
    } catch (error) {
      console.error('Login failed:', error.message);
      alert("Login failed. Please try again.");
    }
  };

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
        <Button
          onClick={handleSpeak}
          variant="contained"
          sx={{ mt: 1, mb: 1 }}
        >
          Read Instructions
        </Button>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
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
            onChange={(e) => setUsername(e.target.value)}
          />
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
            onChange={(e) => setPassword(e.target.value)}
          />
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

export default Login;
