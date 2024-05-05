import React from "react";
import { Link } from "react-router-dom";
import "./homePage.css";


const HomePage = () => {
  return (
    <div>
      {/* Hero Banner */}
      <div className="hero-banner position-relative">
        <img
          src="/static/images/freeroyaltyunsplash.jpg"
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
            fontWeight: "bold"
          }}
        >
          Welcome to Empower Events
        </h1>
      </div>

      {/* Event Previews */}
      <div className="px-4">
        <div className="event-previews row mt-4 justify-content-center">
          <Link to="/events/past" className="col-md-4 text-decoration-none">
            <div className="card hover-effect">
              <img
                src="/static/images/random.jpg"
                className="card-img-top"
                alt="Past Event"
              />
              <div className="card-body">
                <h5 className="card-title">Past Event</h5>
                <p className="card-text">Review or view our past events.</p>
              </div>
            </div>
          </Link>

          <Link to="/events/future" className="col-md-4 text-decoration-none">
            <div className="card hover-effect">
              <img
                src="/static/images/conference.jpg"
                className="card-img-top"
                alt="Future Event"
              />
              <div className="card-body">
                <h5 className="card-title">Future Event</h5>
                <p className="card-text">See our new events.</p>
              </div>
            </div>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <div className="footer row mt-5 bg-light py-3">
        <div className="col-md-4">
          <h5>Contact Us</h5>
          <p>Email: contact@empowerevents.com</p>
          <p>Phone: (123) 456-7890</p>
        </div>
        <div className="col-md-4">
          <h5>Follow Us</h5>
          <a href="https://twitter.com/empowerevents" className="me-2">
            Twitter
          </a>
          <a href="https://facebook.com/empowerevents">Facebook</a>
        </div>
        <div className="col-md-4">
          <h5>About Us</h5>
          <p>Miles Write Something Here.</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
