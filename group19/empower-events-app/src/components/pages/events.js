import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import { GoogleMap, useLoadScript } from "@react-google-maps/api";



const Events = () => {
  const [response, setResponse] = useState([]);
  const { isLoaded } = useLoadScript({    
    googleMapsApiKey: '***REMOVED***',
    });

  useEffect(() => {
    getData();
  }, []);

  // Get json with questions set by charity about event
  const getData = async () => {
    try {
      response = await axios.get("/api/events/");
      console.log(response.data);
    } catch (error) {
      console.error("Error getting events:", error);
    }
  };

  return (
    <div className="Events">
      <div className="justify-content-center mt-5">
        <h1 className="text-center">Events</h1>
      </div>
      {response.map((response) => {
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
                      center={{ lat: response.latitude, lng: response.longitude }}
                      mapContainerClassName='map-container'
                    </GoogleMap>
                  </div>
                </div>
                <div className="col-md-auto">
                  <div className="card-body">
                    <h2 className="card-title">{response.description}</h2>
                    <p className="card-text">Age group: {response.age_group}</p>
                    <p className="card-text">Date: {response.date}</p>
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

