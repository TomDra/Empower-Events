import { React, useEffect, useState } from "react";
import axios from "axios";
import { GoogleMap, useLoadScript } from "@react-google-maps/api";
window.google = window.google ? window.google : {};

const Events = () => {
  const [responseData, setResponseData] = useState("");
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "***REMOVED***",
  });
  const currentURL = window.location.href;

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response;
        if (currentURL.includes("past")) {
          response = await axios.get(
            "http://localhost:8000/api/events/previous-list/?page=1"
          );
        } else {
          response = await axios.get(
            "http://localhost:8000/api/events/upcoming-list/?page=1"
          );
        }
        setResponseData(response.data);
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  if (!isLoaded) return "Loading maps";
  if (!responseData) return <div>Loading...</div>;
  return (
    <div className="Events">
      <div className="justify-content-center mt-5">
        <h1 className="text-center">Events</h1>
      </div>
      {responseData.results.map((event) => (
        <div className="container px-4" key={event.event_id}>
          <div className="card mb-3 text-start" style={{ maxWidth: "auto" }}>
            <div className="row g-0">
              <div className="col-md-2 d-flex justify-content-center align-items-center mr-1">
                <div className="ratio ratio-1x1">
                  <GoogleMap
                    zoom={9}
                    center={{
                      lat: parseFloat(event.latitude),
                      lng: parseFloat(event.longitude),
                    }}
                    mapContainerStyle={{ width: "100%", height: "100%" }}
                  />
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
      ))}
      {responseData && responseData.next && (
        <div className="btn btn-primary">
          <a href={responseData.next}>Next page</a>
        </div>
      )}
    </div>
  );
};

export default Events;
