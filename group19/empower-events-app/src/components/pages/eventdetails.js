/* global google */
import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Loader } from "@googlemaps/js-api-loader";

const EventDetailPage = () => {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const mapRef = useRef(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/events/${eventId}/`)
      .then(response => response.json())
      .then(data => {
        console.log("Fetched event data:", data);
        setEvent(data);
        loadMap(data);
      })
      .catch(error => console.error('Error fetching event details:', error));
  }, [eventId]);

  const loadMap = (eventData) => {
    const lat = parseFloat(eventData.latitude);
    const lng = parseFloat(eventData.longitude);

    if (isNaN(lat) || isNaN(lng)) {
      console.error("Invalid coordinates:", eventData.latitude, eventData.longitude);
      return;
    }

    const loader = new Loader({
      apiKey: "***REMOVED***",
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
    <div className="event-detail-container">
      <h1>{event.description}</h1>
      <img src={event.image || 'defaultImagePath.jpg'} alt="Event Cover" />
      <p><strong>Charity:</strong> {event.charity_name}</p>
      <p><strong>Compatible Disabilities:</strong> {event.compatible_disabilities.join(", ")}</p>
      <div ref={mapRef} style={{ width: '400px', height: '300px' }} />
    </div>
  );
};

export default EventDetailPage;
