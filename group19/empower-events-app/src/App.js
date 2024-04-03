import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import HelloWorld from "./HelloWorld";
import Login from "./components/pages/login";
import Events from "./components/pages/events";
import EventsTest from "./components/pages/eventscopy.js";
import "./App.css";
import { useEffect, useState } from "react";

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HelloWorld />} />
          <Route path="/login" element={<Login />} />
          <Route path="/events" element={<Events />} />
          <Route path="/test" element={<EventsTest />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}


export default App;
