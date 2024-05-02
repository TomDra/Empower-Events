/* global google */
import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Loader } from "@googlemaps/js-api-loader";
import './eventdetails.css';  // Import the stylesheet

const EventDetailPage = () => {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const mapRef = useRef(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/events/${eventId}/`)
      .then(response => response.json())
      .then((data) => {
        console.log("Fetched event data:", data);
        setEvent(data);
        loadMap(data);
      })
      .catch(error => console.error('Error fetching event details:', error));
  }, [eventId]);

  const loadMap = (eventData) => {
    const lat = parseFloat(eventData?.latitude);
    const lng = parseFloat(eventData?.longitude);

    if (isNaN(lat) || isNaN(lng)) {
      console.error("Invalid coordinates:", eventData?.latitude, eventData?.longitude);
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
      });
    });
  };

  if (!event) {
    return <div>Loading...</div>;
  }

  return (
    <div className="event-detail-page">
      <div className="photo-container">
        <img src={event?.image || '/static/images/mic.jpg'} alt="Event Cover" className="event-image" />
        <div className="text-overlay">
          <h1 className="event-title">{event?.description}</h1>
          <p className="event-description">Join us at this event to make a positive impact and enjoy a great time!</p>
        </div>
      </div>

      <div className="event-info-containers">
        <div className="event-info-card">
          <p><strong>Charity:</strong> {event?.charity_name}</p>
        </div>

        <div className="event-info-card">
          <p><strong>Compatible Disabilities:</strong> {event?.compatible_disabilities.join(", ")}</p>
        </div>

        <div className="event-info-card">
          <p><strong>Age Group:</strong> {event?.age_group.title} ({event?.age_group.lower} - {event?.age_group.higher} years old)</p>
        </div>
      </div>

      <button className="btn-primary">Book Now</button>

      <div ref={mapRef} className="map" />

      <div className="event-feedback">
        <p><strong>Feedback:</strong></p>
        <ul>
          {event?.feedback.map((feedback, index) => (
            <li key={index}>{feedback}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default EventDetailPage;
