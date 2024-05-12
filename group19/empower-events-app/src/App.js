// Import the necessary components
import React, { useState } from 'react';
import axios from "axios";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/pages/login";
import SignUp from "./components/pages/signup";
import HomePage from "./components/pages/homePage";
import Events from "./components/pages/events";
import CharityLogin from "./components/pages/charityLogIn";
import Feedback from "./components/pages/feedback";
import EventDetailPage from "./components/pages/eventdetails";
import AddEvents from "./components/pages/add-events"; // Make sure the path is correct
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
              <Route path="/charity/login" element={<CharityLogin onLogin={handleLogin} />} />
              <Route path="/events/:eventId" element={<EventDetailPage />} />
              <Route path="/events/past" element={<Events />} />
              <Route path="/events/future" element={<Events />} />
              <Route path="/feedback/:id" element={<Feedback />} />
              <Route path="/add-event" element={<AddEvents />} /> {/* New route for adding events */}
            </Routes>
          </div>
          <Footer />
        </BrowserRouter>
      </UserProvider>
    </div>
  );
};

export default App;
