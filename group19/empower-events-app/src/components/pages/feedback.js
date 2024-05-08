import React, { useState, useEffect } from "react";
import axios from "axios";
import Recorder from "mic-recorder-to-mp3";
import { useParams } from "react-router-dom";

const recorder = new Recorder({
  bitRate: 128,
});

const FeedbackForm = ({ match }) => {
  const [responseData, setResponseData] = useState([]);
  const [activityFeedback, setActivityFeedback] = useState([]);
  const [leaderFeedback, setLeaderFeedback] = useState("");
  const [radioOptions, setRadioOptions] = useState([]);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [audioBlob, setAudioBlob] = useState(null);
  const [permission, setPermission] = useState(false);
  const { id } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response;
        response = await axios.get(
          `http://localhost:8000/api/feedback/${id}/feedback-questions-list`
        );
        setResponseData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [id]);

  const handleOptionChange = (questionIndex, optionValue) => {
    setRadioOptions((radioOptions) => ({
      ...radioOptions,
      [questionIndex]: optionValue,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      .split("=")[1];

    const formData = new FormData();
    formData.append("audio", audioBlob, `recording${id}.mp3`);
    formData.append("activity_id", id);
    formData.append("activityFeedback", activityFeedback);
    formData.append("leaderFeedback", leaderFeedback);
    formData.append("questionAnswers", JSON.stringify(radioOptions));
    formData.append("feedbackQuestions", JSON.stringify(responseData));

    try {
      await axios.post(
        `http://localhost:8000/api/feedback/${id}/feedback-submission`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-CSRFToken": csrfToken,
          },
        }
      );
      console.log("Feedback submitted successfully");
    } catch (error) {
      console.error("Error submitting feedback:", error);
    }
  };

  const getMicrophonePermission = async () => {
    if ("MediaRecorder" in window) {
      try {
        const streamData = await navigator.mediaDevices.getUserMedia({
          audio: true,
          video: false,
        });
        setPermission(true);
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert("The MediaRecorder API is not supported in your browser.");
    }
  };

  const startRecording = async () => {
    recorder
      .start()
      .then(() => {
        setRecordingStatus("recording");
      })
      .catch((err) => {
        console.error("Failed to start recording: ", err);
      });
  };

  const stopRecording = () => {
    setRecordingStatus("inactive");
    recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        console.log("Recording stopped");
        setAudioBlob(blob);
      })
      .catch((err) => {
        console.error("Failed to get MP3: ", err);
      });
  };

  if (!responseData) return <div>Loading...</div>;

  return (
    <div className="Feedback pt-4 container">
      <h1>Feedback for {responseData.description}</h1>
      <form onSubmit={handleSubmit}>
        {responseData.map((question, index) => (
          <div className="row justify-content-center">
            <div className="card mb-3 text-start">
              <h5 className="card-title">{question.question}</h5>
              <div className="card-body btn-group">
                <input
                  type="radio"
                  className="btn-check m-1"
                  name={`btnradio${index}`}
                  id={`btnradio${index}1`}
                  autoComplete="off"
                  value="positive"
                  checked={radioOptions[index] === "positive"}
                  onChange={() => handleOptionChange(index, "positive")}
                />
                <label
                  className="btn btn-outline-success bi bi-emoji-smile fs-1 "
                  htmlFor={`btnradio${index}1`}
                ></label>

                <input
                  type="radio"
                  className="btn-check m-1"
                  name={`btnradio${index}`}
                  id={`btnradio${index}2`}
                  autoComplete="off"
                  value="negative"
                  checked={radioOptions[index] === "negative"}
                  onChange={() => handleOptionChange(index, "negative")}
                />
                <label
                  className="btn btn-outline-danger bi bi-emoji-frown fs-1"
                  htmlFor={`btnradio${index}2`}
                ></label>
              </div>
            </div>
          </div>
        ))}
        <div className="audio-controls">
          {!permission ? (
            <button
              onClick={getMicrophonePermission}
              type="button"
              className="bi bi-plus-circle btn btn-primary p-4 m-3 fs-4"
            >
              Get Microphone
            </button>
          ) : null}
          {permission && recordingStatus === "inactive" ? (
            <button
              onClick={startRecording}
              type="button"
              className="bi bi-mic btn btn-success p-4 m-3 fs-4"
            >
              Start Recording
            </button>
          ) : null}
          {recordingStatus === "recording" ? (
            <button
              onClick={stopRecording}
              type="button"
              className="bi bi-mic-mute btn btn-danger p-4 m-3 fs-4"
            >
              Stop Recording
            </button>
          ) : null}
          <div>
            {audioBlob ? (
              <audio src={URL.createObjectURL(audioBlob)} controls></audio>
            ) : null}
          </div>
        </div>
        <div className="form-floating">
          <textarea
            name="general-feedback"
            className="form-control"
            id="TextAreaActivity"
            style={{ height: "100px" }}
            onChange={(e) => setActivityFeedback(e.target.value)}
          ></textarea>
          <label htmlFor="TextAreaActivity">Type general feedback here</label>
        </div>
        <div className="form-floating">
          <textarea
            name="general-feedback"
            className="form-control"
            id="TextAreaLeader"
            style={{ height: "100px" }}
            onChange={(e) => setLeaderFeedback(e.target.value)}
          ></textarea>
          <label htmlFor="TextAreaLeader">Type leader feedback here</label>
        </div>
        <button type="Submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
};

export default FeedbackForm;
