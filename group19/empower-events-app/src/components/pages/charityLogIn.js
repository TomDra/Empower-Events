import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, TextField, Typography, Container, Box } from '@mui/material';
import { UserContext } from '../../contexts/userContext';

function CharityLogin() {
  const [charity_name, setCharity_name] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { handleLogin } = useContext(UserContext);

  const handleCharityLogin = async (event) => {
    event.preventDefault();
    setError(''); // Reset error message on new login attempt
  
    try {
      const response = await fetch('http://localhost:8000/api/charity/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ charity_name, password })
      });
  
      if (!response.ok) {
        throw new Error('Login failed!');
      }
  
      const data = await response.json();
      console.log('Login successful:', data);
      // You might want to save the token to localStorage and redirect the user
      localStorage.setItem('charityToken', data.token);
      //alert('Login successful! Token stored in localStorage');
      

      // handleLogin();  ## todo: handlelogin knows if its  a charity or user

      // Redirect to the dashboard or wherever needed
      navigate("/charity/home");
    } catch (error) {
      console.error('Login error:', error);
      setError(error.message);
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
        <Typography component="h1" variant="h5">Charity Sign In</Typography>
        <Box component="form" onSubmit={handleCharityLogin} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="charity_name"
            label="Charity name:"
            name="charity_name"
            autoComplete="charity_name"
            autoFocus
            value={charity_name}
            onChange={(e) => setCharity_name(e.target.value)}
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
      </Box>
    </Container>
  );
  };

export default CharityLogin;
