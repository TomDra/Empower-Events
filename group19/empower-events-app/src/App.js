// src/App.js
import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ContactUs from './components/pages/contactus';
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
import AddEvents from "./components/pages/add-events";
import NavigationBar from "./components/NavigationBar";
import LeaderVote from "./components/pages/leaderVote";
import ViewLeaderVote from "./components/pages/viewLeaderVote";
import Footer from "./components/footer";
import { UserProvider } from './contexts/userContext';
import WeatherNotification from './components/Weather'; // Import the WeatherNotification component
import "./App.css";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  const userLatitude = "51.5074"; // Example latitude (London)
  const userLongitude = "-0.1278"; // Example longitude (London)

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
              <Route path="/contact-us" element={<ContactUs />} />
              <Route path="/leader-vote" element={<LeaderVote />} />
              <Route path="/admin/leader-votes" element={<ViewLeaderVote />} />
              <Route path="/admin/add-event" element={<AddEvents />} />
              {/* Add other routes as needed */}
            </Routes>
          </div>
          <Footer />
          <WeatherNotification lat={userLatitude} lon={userLongitude} /> {/* Include the WeatherNotification component */}
        </BrowserRouter>
      </UserProvider>
    </div>
  );
};

export default App;
