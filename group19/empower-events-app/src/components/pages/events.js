import React from "react";
import axios from "axios";

const Events = () => {
  //   try {
  //     axios.get("http://localhost:8000/api/events/").then((response) => {
  //       const data = response.data;
  //     });
  //   } catch (error) {
  //     console.log("Error:", error);
  //   }

  return (
    <div className="container px-4">
      <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
      <div className="row justify-content-center mt-5">
        <h1 className="text-center">Events</h1>
      </div>
      <div className="card mb-3 text-start" style={{ maxWidth: "auto" }}>
        <div className="row g-0">
          <div className="col-md-2 d-flex justify-content-center align-items-center mr-1">
            <div className="ratio ratio-1x1 ">
              <iframe
                width="auto"
                height="auto"
                style={{ border: "0" }}
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                pointer-events="none"
                src="https://maps.google.com/maps?q=40.7128,-74.0060&z=15&output=embed"
              ></iframe>
            </div>
          </div>
          <div className="col-md-auto">
            <div className="card-body">
              <h2 className="card-title">Outdoor Sports Events</h2>
              <p className="card-text">Age group: Teens</p>
              <p className="card-text">Date: 01-01-01 4:00</p>
              <a href="#" className="btn btn-primary">
                View More
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Events;
