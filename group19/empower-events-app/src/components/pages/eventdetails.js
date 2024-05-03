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
    fetch(`http://localhost:8000/api/events/detail/${eventId}/`)
      .then(response => response.json())
      .then((data) => {
        console.log("Fetched event data:", data);
        setEvent(data);
        loadMap(data.activity); // Updated to pass activity data to loadMap
      })
      .catch(error => console.error('Error fetching event details:', error));
  }, [eventId]);

  const loadMap = (activityData) => { // Updated to receive activityData
    const lat = parseFloat(activityData.latitude);
    const lng = parseFloat(activityData.longitude);

    if (isNaN(lat) || isNaN(lng)) {
      console.error("Invalid coordinates:", activityData.latitude, activityData.longitude);
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
        <img src={event.activity.image || '/static/images/mic.jpg'} alt="Event Cover" className="event-image" />
        <div className="text-overlay">
          <h1 className="event-title">{event.activity.description}</h1> {/* Updated to access activity description */}
          <p className="event-description">Join us at this event to make a positive impact and enjoy a great time!</p>
          <p className="event-time">{event.timeDate}</p>
        </div>
      </div>

      <div className="event-info-containers">
        <div className="event-info-card">
          <p><strong>Charity:</strong> {event.charity.name}</p> {/* Updated to access charity name */}
        </div>

        <div className="event-info-card">
          <p><strong>Compatible Disabilities:</strong> {event.activity.compatible_disabilities.join(", ")}</p> {/* Updated to access activity compatible disabilities */}
        </div>

        <div className="event-info-card">
          <p><strong>Age Group:</strong> {event.activity.age_group.title} ({event.activity.age_group.lower} - {event.activity.age_group.higher} years old)</p> {/* Updated to access activity age group */}
        </div>
      </div>

      <button className="btn-primary">Book Now</button>

      <div ref={mapRef} className="map" />

    </div>
  );
};

export default EventDetailPage;
