import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import { GoogleMap, useLoadScript } from "@react-google-maps/api";
import { Button, TextField, Typography, Container, Box } from "@mui/material";
import { speak } from "../../utils/CheckSpeech";
window.google = window.google ? window.google : {};


const Events = () => {
  const [responseData, setResponseData] = useState("");
  const location = useLocation();
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "***REMOVED***",
  });
  const currentURL = window.location.href;

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

  useEffect(() => {
    fetchData();
  }, [location]);

  const handleSpeak = (event) => {
    speak(""+event.title+"... "+event.description+". Date and time: "+Date(event.date).toLocaleString());
    speak("The event age group is for"+event.age_group);
  };

  if (!isLoaded) return "Loading maps";
  if (!responseData) return <div>ERROR please refresh</div>;
  return (
    <div className="Events">
      <div className="justify-content-center mt-5">
        <h1 className="text-center">Events</h1>
      </div>
      {responseData.results.map((event) => (
        <div className="container px-4" key={event.event_id}>
          <div className="card mb-3 text-start" style={{ maxWidth: "auto" }}>
            <div className="row g-0">
              <div className="col-md-2 d-flex justify-content-center align-items-center">
                <div className="ratio ratio-1x1">
                  {/* Ensure event.photo_file_path is constructed properly */}
                  <img src={`http://localhost:8000/media/activity_images/${event.photo_file_path}`} alt="Event photo" style={{ height: "100%" }} />
                </div>
              </div>
              <div className="col-md-8">
                <div className="card-body">
                  <h2 className="card-title">{event.title}</h2>
                  <h6 className="card-title">{event.description}</h6>
                  <p className="card-text">Age group: {event.age_group}</p>
                  <p className="card-text">{Date(event.date).toLocaleString()}</p>

                  <a href={"/events/" + event.event_id} className="btn btn-primary">
                    View More
                  </a>
                  {currentURL.includes("past") ? (
                    <a href={"/feedback/" + event.event_id} className="btn btn-primary">
                      Give Feedback
                    </a>
                  ) : null}
                  {currentURL.includes("future") ? (
                  <a href={"/register-interest/" + event.event_id} className="btn btn-primary">
                      Resister your interest
                    </a>
                   ) : null}

                </div>
              </div>
              <div className="col-md-2 d-flex justify-content-center align-items-center">
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
                   <Button
                      onClick={() => handleSpeak(event)}
                      variant="contained"
                      sx={{ mt: 1, mb: 1 }}
                       title="Read Details"
                       size="lg"
                    >
                  <strong>Read Details</strong>
                  <img src="/static/images/text_to_speech_icon.png" alt="Speech Icon" />
                </Button>
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
