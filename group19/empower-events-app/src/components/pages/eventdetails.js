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
    <div className="container event-detail-container">
      <h1 className="text-center">{event.description}</h1>
      <div className="row">
        <div className="col-md-6">
          <img src={event.image || 'defaultImagePath.jpg'} alt="Event Cover" className="img-fluid rounded" />
        </div>
        <div className="col-md-6">
          <p><strong>Charity:</strong> {event.charity_name}</p>
          <p><strong>Compatible Disabilities:</strong> {event.compatible_disabilities.join(", ")}</p>
          <div ref={mapRef} style={{ width: '100%', height: '300px' }} />
        </div>
      </div>
    </div>
  );
};

export default EventDetailPage;
