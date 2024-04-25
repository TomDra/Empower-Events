import React, { useEffect } from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="container px-4">
      <div className="row justify-content-center mt-5">
        <h1 className="text-center">Welcome to Empower Events</h1>
      </div>
      <div className="row justify-content-center mt-3">
        <a
          href="/events"
          className="col-md-4 btn btn-outline-primary m-5 p-5 fs-1"
        >
          Past Events
        </a>
        <a
          href="/events"
          className="col-md-4 btn btn-outline-primary m-5 p-5 fs-1 "
        >
          Future Events
        </a>
      </div>
    </div>
  );
};

export default HomePage;
