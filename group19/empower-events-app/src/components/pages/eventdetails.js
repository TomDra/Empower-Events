import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const EventDetailPage = () => {
  const { eventId } = useParams(); // Get the event ID from the route parameters
  const [event, setEvent] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/events/${eventId}/`) // Adjust the URL as needed
      .then(response => response.json())
      .then(data => setEvent(data))
      .catch(error => console.error('Error fetching event details:', error));
  }, [eventId]);

  if (!event) {
    return <div>Loading...</div>; // Loading state
  }

  // Format and display event details here
  return (
    <div className="event-detail-container">
      <h1>{event.activity_name}</h1>
      <p>Date: {new Date(event.time).toLocaleString()}</p>
      {/* Add more event details here */}
      <img src={event.image || 'defaultImagePath.jpg'} alt="Event Cover" />
      <p>{event.description}</p>
      {/* ADD map maybe contact aswell */}
    </div>
  );
};

export default EventDetailPage;
