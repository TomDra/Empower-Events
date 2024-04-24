import React from "react";
import axios from "axios";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import HelloWorld from "./HelloWorld";
import Login from "./components/pages/login";
import SignUp from "./components/pages/signup"; // Ensure this path matches where your SignUp component is located
import HomePage from "./components/pages/homePage";
import "./App.css";
import EventDetailPage from "./components/pages/eventdetails"; // Import the EventDetailPage component

const client = axios.create({
  baseURL: "http://localhost:8000",
});

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/events/:eventId" element={<EventDetailPage />} />
          <Route path="/register" element={<SignUp />} />
          <Route path="/test" element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
