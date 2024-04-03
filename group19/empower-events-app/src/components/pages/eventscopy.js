import React from "react";
import axios from "axios";
import data from "./data.json";

const Events = () => {
  //   try {
  //     axios.get("http://localhost:8000/api/events/").then((response) => {
  //       const data = response.data;
  //     });
  //   } catch (error) {
  //     console.log("Error:", error);
  //   }

  function createMapUrl(latitude, longitude) {
    return `https://maps.google.com/maps?q=${latitude},${longitude}&z=15&output=embed`;
  }

  return (
    <div className="Events">
      <div className="justify-content-center mt-5">
        <h1 className="text-center">Events</h1>
      </div>
      {data.map((data) => {
        return (
          <div className="container px-4">
            <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
            <div className="card mb-3 text-start" style={{ maxWidth: "auto" }}>
              <div className="row g-0">
                <div className="col-md-2 d-flex justify-content-center align-items-center mr-1">
                  <div className="ratio ratio-1x1 ">
                    <iframe
                      title="map"
                      width="auto"
                      height="auto"
                      style={{ border: "0" }}
                      loading="lazy"
                      referrerpolicy="no-referrer-when-downgrade"
                      pointer-events="none"
                      src={createMapUrl(data.latitude, data.longitude)}
                    ></iframe>
                  </div>
                </div>
                <div className="col-md-auto">
                  <div className="card-body">
                    <h2 className="card-title">{data.description}</h2>
                    <p className="card-text">Age group: {data.age_group}</p>
                    <p className="card-text">Date: {data.date}</p>
                    <a href="#" className="btn btn-primary">
                      View More
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default Events;
