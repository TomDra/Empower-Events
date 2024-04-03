import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import HelloWorld from "./HelloWorld";
import Login from "./components/pages/login";
import "./App.css";
import EventDetailPage from "./components/pages/eventdetails"; // Import the EventDetailPage component

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HelloWorld />} />
          <Route path="/login" element={<Login />} />
          <Route path="/events/:eventId" element={<EventDetailPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}


export default App;
