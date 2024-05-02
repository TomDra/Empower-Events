// src/App.js
import React, { useState } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import AppNavbar from './components/navbar';
import Login from './components/pages/login';
import SignUp from './components/pages/signup';
import HomePage from './components/pages/homePage';
import { UserProvider } from './contexts/userContext';



const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <UserProvider>
    <BrowserRouter>
      <AppNavbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<SignUp />} />
        <Route path="/test" element={<HomePage />} />
        {/* Add other routes as needed */}
      </Routes>
    </BrowserRouter>
    </UserProvider>
  );
};

export default App;
