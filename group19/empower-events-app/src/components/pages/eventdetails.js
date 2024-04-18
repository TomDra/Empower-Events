import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const EventDetailPage = () => {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/events/${eventId}/`)
      .then(response => response.json())
      .then(data => setEvent(data))
      .catch(error => console.error('Error fetching event details:', error));
  }, [eventId]);

  if (!event) {
    return <div>Loading...</div>;
  }

  const containerStyle = {
    width: '400px',
    height: '300px'
  };

  const center = {
    lat: event.latitude,  
    lng: event.longitude
  };

  return (
    <div className="event-detail-container">
      <h1>{event.description}</h1>
      <img src={event.image || 'defaultImagePath.jpg'} alt="Event Cover" />
      <p><strong>Charity:</strong> {event.charity_name}</p>
      <p><strong>Compatible Disabilities:</strong> {event.compatible_disabilities.join(", ")}</p>
      <LoadScript googleMapsApiKey="AlzaSyD-P1nl2HT0g7Uv3aPvFer0pXAT4blnn90">
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={center}
          zoom={10}
        >
          <Marker position={center} />
        </GoogleMap>
      </LoadScript>
    </div>
  );
};

export default EventDetailPage;
