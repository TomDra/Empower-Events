import React from "react";
import axios from "axios";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import HelloWorld from "./HelloWorld";
import Login from "./components/pages/login";
import SignUp from "./components/pages/signup"; // Ensure this path matches where your SignUp component is located
import HomePage from "./components/pages/homePage";
import Events from "./components/pages/events";
import "./App.css";
import { useEffect, useState } from "react";

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
          <Route path="/register" element={<SignUp />} />
          <Route path="/test" element={<HomePage />} />
          <Route path="/events/future" element={<Events />} />
          <Route path="/events/past" element={<Events />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
