/* global google */
import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Loader } from "@googlemaps/js-api-loader";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './eventdetails.css';

const EventDetailPage = () => {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const mapRef = useRef(null);
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

  const scheduleNotification = (eventDateTime) => {
    const eventTime = new Date(eventDateTime).getTime();
    const now = Date.now();
    const timeUntilEvent = eventTime - now;

    // Notify 24 hours before the event
    if (timeUntilEvent > 86400000) { // 86400000 ms in 24 hours
      notificationTimer.current = setTimeout(() => {
        toast.info(`Reminder: Your event starts in less than 24 hours!`);
      }, timeUntilEvent - 86400000);
    }
  };

  const loadMap = (activityData) => {
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
      });
    });
  };

  if (!event) {
    return <div>Loading...</div>;
  }

  return (
    <div className="event-detail-page">
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <div className="photo-container">
        <img src={event.activity.image || '/static/images/mic.jpg'} alt="Event Cover" className="event-image" />
        <div className="text-overlay">
          <h1 className="event-title">{event.activity.description}</h1>
          <p className="event-description">Join us at this event to make a positive impact and enjoy a great time!</p>
          <p className="event-time">{event.timeDate}</p>
        </div>
      </div>

      <div className="event-info-containers">
        <div className="event-info-card">
          <p><strong>Charity:</strong> {event.charity.name}</p>
        </div>

        <div className="event-info-card">
          <p><strong>Compatible Disabilities:</strong> {event.activity.compatible_disabilities.join(", ")}</p>
        </div>

        <div className="event-info-card">
          <p><strong>Age Group:</strong> {event.activity.age_group.title} ({event.activity.age_group.lower} - {event.activity.age_group.higher} years old)</p>
        </div>
      </div>

      <button className="btn-primary" onClick={() => toast.info("Booking feature coming soon!")}>Book Now</button>

      <div ref={mapRef} className="map" />
    </div>
  );
};

export default EventDetailPage;
