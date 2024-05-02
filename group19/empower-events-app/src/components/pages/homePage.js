import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="container px-4">
      {/* Hero Banner */}
      <div className="hero-banner row justify-content-center mt-5">
        <img
          src="/images/freeroyaltyunsplash.jpg"
          alt="Empower Events"
          className="col-12"
          style={{ height: "300px", objectFit: "cover" }}
        />
        <h1 className="text-center mt-4">Welcome to Empower Events</h1>
      </div>

      {/* Event Previews */}
      <div className="event-previews row mt-4">
        <div className="col-md-4">
          <div class="card">
            <img
              src="/images/past-event.jpg"
              className="card-img-top"
              alt="Past Event"
            />
            <div className="card-body">
              <h5 className="card-title">Past Event: XYZ Conference</h5>
              <p className="card-text">A brief description of a past event.</p>
              <a href="/events/xyz-conference" className="btn btn-primary">
                Learn More
              </a>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div class="card">
            <img
              src="/images/future-event.jpg"
              class="card-img-top"
              alt="Future Event"
            />
            <div className="card-body">
              <h5 className="card-title">Future Event: ABC Summit</h5>
              <p className="card-text">A brief description of an upcoming event.</p>
              <a href="/events/abc-summit" className="btn btn-primary">
                Learn More
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Image Gallery */}
      <div className="image-gallery row justify-content-center mt-5">
        <div className="col-md-6">
          <img
            src="/images/gallery1.jpg"
            alt="Event Image 1"
            className="img-fluid"
          />
        </div>
        <div class="col-md-6">
          <img
            src="/images/gallery2.jpg"
            alt="Event Image 2"
            className="img-fluid"
          />
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
        <div class="col-md-4">
          <h5>About Us</h5>
          <p>A brief description of the organization and its mission.</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
