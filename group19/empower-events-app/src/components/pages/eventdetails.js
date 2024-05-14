/* global google */
import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Loader } from "@googlemaps/js-api-loader";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './eventdetails.css';
import { speak } from "../../utils/CheckSpeech";
import { Button, TextField, Typography, Container, Box } from "@mui/material";

const EventDetailPage = () => {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const mapRef = useRef(null);
  const [geoapifyData, setGeoapifyData] = useState(null);


  const notificationTimer = useRef(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/events/detail/${eventId}/`)
      .then(response => response.json())
      .then((data) => {
        setEvent(data);
        scheduleNotification(data.time); // Assuming 'data.time' is ISO string of event datetime
        loadMap(data.activity);
      })
      .catch(error => {
        console.error('Error fetching event details:', error);
        toast.error('Failed to fetch event details.');
      });

    return () => {
      if (notificationTimer.current) {
        clearTimeout(notificationTimer.current);
      }
    };
  }, [eventId]);

  var requestOptions = {
      method: 'GET',
    };

    useEffect(() => {
      if (event) {
        fetch("https://api.geoapify.com/v1/geocode/reverse?lat=" + event.activity.latitude + "&lon=" + event.activity.longitude + "&apiKey=e523fb9420a94cd4a8b01dcc407e6164", requestOptions)
          .then(response => response.json())
          .then(result => setGeoapifyData(result))
          .catch(error => console.log(error + 'error', error));
      }
    }, [event]);
  const handleSpeak = () => {
    // Reading out the welcome message and input field descriptions
    speak("Title: "+event.activity.title+". DESCRIPTION: "+event.activity.description+". Date and time: "+event.timeDate.split('|')[0]+", at "+event.timeDate.split('|')[1]);
    speak(". This event is compatible with these disabilities: "+event.activity.compatible_disabilities.join(", ")+". The age group is "+event.activity.age_group.title+" ("+event.activity.age_group.lower+" - "+event.activity.age_group.higher+" years old)");
    speak(". This event is run by: "+event.event_leader.name+", with Charity:"+event.charity.name)
    speak(". The location of the event is "+ geoapifyData.features[0].properties.formatted)
  };


  const loadMap = (activityData) => { // Updated to receive activityData
    const lat = parseFloat(activityData.latitude);
    const lng = parseFloat(activityData.longitude);

    if (isNaN(lat) || isNaN(lng)) {
      console.error("Invalid coordinates:", activityData.latitude, activityData.longitude);
      toast.error('Invalid coordinates provided.');
      return;
    }

    const loader = new Loader({
      apiKey: "***REMOVED***", // Replace with your actual API key
      version: "weekly",
    });

    loader.load().then(() => {
        const center = { lat, lng };
        const map = new google.maps.Map(mapRef.current, {
            center,
            zoom: 10,
        });
        new google.maps.Marker({
            position: center,
            map,
            title: activityData.title,
        });
        const infoWindow = new google.maps.InfoWindow({
            content: `<div>
                        <h2>${activityData.title}</h2>
                        <p>${activityData.description}</p>
                        <p><strong>Charity:</strong> ${activityData.charityName}</p>
                        <p><strong>Compatible Disabilities:</strong> ${activityData.compatible_disabilities.join(", ")}</p>
                        <p><strong>Age Group:</strong> ${activityData.age_group.title} (${activityData.age_group.lower} - ${activityData.age_group.higher} years old)</p>
                     </div>`,
        });
        map.addListener("click", () => {
            infoWindow.open(map);
        });
    });

  };


  
  if (!event) {
    return <div>ERROR Please refresh</div>;
  }
  const dateString = event.timeDate_readable;
  //console.log(new Date(dateString).toString());
  //const formattedDate = new Date(dateString).toString();
  return (
    <div className="event-detail-page">
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <div className="photo-container">
        <img src={`http://localhost:8000/media/activity_images/${event.activity.photo_file_path}`} alt="Event Cover" className="event-image" />
        <div className="text-overlay">
          <h1 className="event-title">{event.activity.title}</h1> 
          <p className="event-description">{event.activity.description}</p>
          <p className="event-time">{dateString}</p>
        </div>
      </div>
      <Button
          onClick={handleSpeak}
          variant="contained"
          sx={{ mt: 1, mb: 1 }}
        >
          Read Event Details
          <img src="/static/images/text_to_speech_icon.png" alt="Speech Icon" />
        </Button>

      <div className="event-info-containers">
        <div className="event-info-card">
          <p><strong>Charity:</strong> {event.charity.name}</p> {/* Updated to access charity name */}
          {event && event.event_leader && (
            <>
              <p><strong>Event leader:</strong> {event.event_leader.name} </p>
              <p><strong>leader's email:</strong> {event.event_leader.email} </p>
            </>
          )}
        </div>

        <div className="event-info-card">
          <p><strong>Compatible Disabilities:</strong> {event.activity.compatible_disabilities.join(", ")}</p> {/* Updated to access activity compatible disabilities */}
          <p><strong>Age Group:</strong> {event.activity.age_group.title} ({event.activity.age_group.lower} - {event.activity.age_group.higher} years old)</p> {/* Updated to access activity age group */}
        </div>

        <div className="event-info-card">
          {geoapifyData && (
          <>
          <p><strong>Location:</strong> {geoapifyData.features[0].properties.formatted}</p>
          </>
          )}
        </div>
      </div>
      {new Date(event.timeDate) < new Date() ? (
        <a href={"/feedback/" + eventId} className="btn-primary">
          Give Feedback
        </a>
      ) : (
        <a href={"/register-interest/" + eventId} className="btn-primary">
          Register your Interest
        </a>
      )}
       <br/>
      <div ref={mapRef} className="map" />
    </div>
  );
};

export default EventDetailPage;
