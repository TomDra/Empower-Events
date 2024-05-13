import React from "react";
import { Link } from "react-router-dom";
import "./homePage.css";

const Portal = () => {
  return (
    <div>
      {/* Hero Banner */}
      <div className="hero-banner position-relative">
        <img
          src="/static/images/conference.jpg"
          alt="Empower Events"
          className="col-12 w-full cover"
          style={{ height: "400px", objectFit: "cover" }}
        />
        <h1
          className="text-center position-absolute w-100 text-white"
          style={{
            top: "40%",
            transform: "translateY(-50%)",
            fontSize: "2.5rem",
            fontWeight: "bold",
          }}
        >
          Admin Portal
        </h1>
      </div>

      {/* Event Previews */}
      <div className="px-4">
        <div className="event-previews row mt-4 justify-content-center">
          <Link to="/admin/add-event" className="col-md-4 text-decoration-none">
            <div className="card hover-effect" id="homePageCard">
              <img
                src="/static/images/freeroyaltyunsplash.jpg"
                className="card-img-top"
                alt="Past Event"
              />
              <div className="card-body">
                <h5 className="card-title">Create Event</h5>
                <p className="card-text">Create a new event</p>
              </div>
            </div>
          </Link>

          <Link to="/admin/events" className="col-md-4 text-decoration-none">
            <div className="card hover-effect" id="homePageCard">
              <img
                src="/static/images/mic.jpg"
                className="card-img-top"
                alt="Future Event"
              />
              <div className="card-body">
                <h5 className="card-title">Feedback</h5>
                <p className="card-text">View feedback on past events</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Portal;
