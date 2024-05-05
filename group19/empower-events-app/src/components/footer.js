// src/components/Footer.js
import React from "react";
import { Link } from "react-router-dom";
import "./footer.css";

const Footer = () => {
  return (
    <div className="footer row mt-5 bg-light py-3">
      <div className="col-md-4">
        <h5>Contact Us</h5>
        <p>Email: contact@empowerevents.com</p>
        <p>Phone: (123) 456-7890</p>
      </div>
      <div className="col-md-4">
        <h5>Follow Us</h5>
        <Link to="https://twitter.com/empowerevents" className="me-2">
          Twitter
        </Link>
        <Link to="https://facebook.com/empowerevents">
          Facebook
        </Link>
      </div>
      <div className="col-md-4">
        <h5>About Us</h5>
        <p>Miles Write Something Here.</p>
      </div>
    </div>
  );
};

export default Footer;
