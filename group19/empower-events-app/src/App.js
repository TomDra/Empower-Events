import React from "react";
import axios from "axios";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import HelloWorld from "./HelloWorld";
import Login from "./components/pages/login";
import HomePage from "./components/pages/homePage";
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
          <Route path="/test" element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
