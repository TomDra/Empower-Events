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
        <p>Phone: +44 7428 423491</p>
      </div>
      <div className="col-md-4">
        <h5>Follow Us</h5>
        <Link to="https://twitter.com/empowerevents" className="me-2">
          Twitter
        </Link>
        <Link to="https://facebook.com/empowerevents">
          Facebook
        </Link>
        <div/>
        <h5>Partners</h5>
        <Link to="https://www.halowproject.org.uk/" className="me-2">
          Halow
        </Link>
      </div>
      <div className="col-md-4">
        <h5>About Us</h5>
        <p>A unique blend of activities, giving people the chance to enjoy an active social life, make new friends, find further education and employment training.</p>
      </div>
    </div>
  );
};

export default Footer;
