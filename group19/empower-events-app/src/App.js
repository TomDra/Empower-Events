//import React from "react";
import axios from "axios";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Login from "./components/pages/login";
import SignUp from "./components/pages/signup";
import HomePage from "./components/pages/homePage";
import Events from "./components/pages/events";
import Feedback from "./components/pages/feedback";
import "./App.css";
import EventDetailPage from "./components/pages/eventdetails";
// src/App.js
import React, { useEffect, useState } from 'react';
//import { Routes, Route, BrowserRouter } from 'react-router-dom';
import AppNavbar from './components/navbar';
import Footer from "./components/footer";
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
  <div className="App">
    <UserProvider>
    <BrowserRouter>
      <AppNavbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
      <div className="content-wrapper">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<SignUp />} />
        <Route path="/test" element={<HomePage />} />
        <Route path="/events/:eventId" element={<EventDetailPage />} />
        <Route key="past" path="/events/past" element={<Events />} />
        <Route key="future" path="/events/future" element={<Events />} />
        {/* Add other routes as needed */}
      </Routes>
      </div>
      <Footer />
    </BrowserRouter>
    </UserProvider>
    </div>
  );
};

export default App;
