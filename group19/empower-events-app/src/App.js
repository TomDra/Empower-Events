import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import HelloWorld from "./HelloWorld";
import Login from "./components/pages/login";
import SignUp from "./components/pages/signup"; // Ensure this path matches where your SignUp component is located
import "./App.css";
import { useEffect, useState } from "react";

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HelloWorld />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<SignUp />} /> {/* Enshallah add this line */}
        </Routes>
      </BrowserRouter>
    </div>
  );
}


export default App;
