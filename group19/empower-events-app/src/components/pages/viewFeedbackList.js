import React, { useEffect, useState } from "react";
import axios from "axios";
window.google = window.google ? window.google : {};

const AdminEvents = () => {
  const [responseData, setResponseData] = useState("");

  const fetchData = async () => {
    try {
      let response;
        response = await axios.get(
          "http://localhost:8000/api/events/previous-list/?page=1"
        );
      setResponseData(response.data);
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

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
              <div className="col-md-2 d-flex justify-content-center align-items-center">
                <div className="ratio ratio-1x1">
                  {/* Ensure event.photo_file_path is constructed properly */}
                  <img
                    src={`http://localhost:8000/media/activity_images/${event.photo_file_path}`}
                    alt="Event photo"
                    style={{ height: "100%" }}
                  />
                </div>
              </div>
              <div className="col-md-8">
                <div className="card-body">
                  <h2 className="card-title">{event.title}</h2>
                  <h6 className="card-title">{event.description}</h6>
                  <p className="card-text">Age group: {event.age_group}</p>
                  <p className="card-text">Date: {event.date}</p>
                  <a
                    href={"/admin/feedback/" + event.event_id}
                    className="btn btn-primary"
                  >
                    View Feedback
                  </a>
                </div>
              </div>
              <div className="col-md-2 d-flex justify-content-center align-items-center">
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

export default AdminEvents;
