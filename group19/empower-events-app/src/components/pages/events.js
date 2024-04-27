import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import { GoogleMap, useLoadScript } from "@react-google-maps/api";

const Events = () => {
  const [responseData, setResponseData] = useState(null);
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "***REMOVED***",
  });

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/events/upcoming-list/?page=1")
      .then((response) => {
        setResponseData(response.data);
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div className="Events">
      <div className="justify-content-center mt-5">
        <h1 className="text-center">Events</h1>
      </div>
      {responseData.results.map((event) => {
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
                    ></iframe>
                    <GoogleMap>
                      zoom={9}
                      center={{ lat: event.latitude, lng: event.longitude }}
                      mapContainerClassName='map-container'
                    </GoogleMap>
                  </div>
                </div>
                <div className="col-md-auto">
                  <div className="card-body">
                    <h2 className="card-title">{event.description}</h2>
                    <p className="card-text">Age group: {event.age_group}</p>
                    <p className="card-text">Date: {event.date}</p>
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
