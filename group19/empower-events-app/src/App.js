// src/App.js
//import React from "react";
import axios from "axios";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import ContactUs from './components/pages/contactus';
import React, { useEffect, useState } from 'react';
import Footer from "./components/footer";
import { UserProvider } from './contexts/userContext';
import HomePage from "./components/pages/homePage";
import Login from "./components/pages/login";
import SignUp from "./components/pages/signup";
import Events from "./components/pages/events";
import Feedback from "./components/pages/feedback";
import AdminPortal from "./components/pages/charityPortal";
import AdminEvents from "./components/pages/viewFeedbackList";
import AdminFeedback from "./components/pages/viewFeedbackDetail";
import CharityLogin from "./components/pages/charityLogIn";
import EventDetailPage from "./components/pages/eventdetails";
import NavigationBar from "./components/NavigationBar";
import LeaderVote from "./components/pages/leaderVote";
import ViewLeaderVote from "./components/pages/viewLeaderVote";
import "./App.css";




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
          <NavigationBar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
          <div className="content-wrapper">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<Login onLogin={handleLogin} />} />
              <Route path="/register" element={<SignUp />} />
              <Route path="/charity/login" element={<CharityLogin onLogin={handleLogin}/>} />
              <Route path="/test" element={<HomePage />} />
              <Route path="/events/:eventId" element={<EventDetailPage />} />
              <Route key="past" path="/events/past" element={<Events />} />
              <Route key="future" path="/events/future" element={<Events />} />
              <Route path="/feedback/:eventId" element={<Feedback />} />
              <Route path="/admin/portal" element={<AdminPortal />} />
              <Route path="/admin/events" element={<AdminEvents />} />
              <Route path="/admin/feedback/:eventId" element={<AdminFeedback />} />
              <Route path="/contact-us" element={<ContactUs />} />  {/* New Contact Us route */}
              <Route path="/leader-vote" element={<LeaderVote />} />
              <Route path="/admin/leader-votes" element={<ViewLeaderVote />} />
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
