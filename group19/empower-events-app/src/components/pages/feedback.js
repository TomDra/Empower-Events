import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const mimeType = "audio/wav";

function FeedbackForm() {
  const [feedback, setFeedback] = useState("");
  const [permission, setPermission] = useState(false);
  const [stream, setStream] = useState(null);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [audioChunks, setAudioChunks] = useState([]);
  const [audio, setAudio] = useState(null);
  const mediaRecorder = useRef(null);

// Get json with questions set by charity about event
  // const getData = async () => {
  //   try {
  //     const response = await axios.get("/api/feedback");
  //     console.log(response.data);
  //   } catch (error) {
  //     console.error("Error getting feedback:", error);
  //   }
  // };
// post data of feedback to the server
  // const postData = async () => {
  //   try {
  //     await axios.post("/api/feedback", { feedback });
  //     console.log("Feedback submitted successfully");
  //   } catch (error) {
  //     console.error("Error submitting feedback:", error);
  //   }
  // };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/api/feedback", { feedback });
      console.log("Feedback submitted successfully");
      setFeedback("");
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
        setStream(streamData);
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert("The MediaRecorder API is not supported in your browser.");
    }
  };

  const startRecording = async () => {
    setRecordingStatus("recording");
    const media = new MediaRecorder(stream, { type: mimeType });
    mediaRecorder.current = media;
    mediaRecorder.current.start();
    let localaudioChunks = [];
    mediaRecorder.current.ondataavailable = (event) => {
      if (typeof event.data === "undefined") return;
      if (event.data.size === 0) return;
      localaudioChunks.push(event.data);
    };
    setAudioChunks(localaudioChunks);
  };

  const stopRecording = () => {
    setRecordingStatus("inactive");
    //stops the recording instance
    mediaRecorder.current.stop();
    mediaRecorder.current.onstop = () => {
      //creates a blob file from the audiochunks data
      const audioBlob = new Blob(audioChunks, { type: mimeType });
      //creates a playable URL from the blob file.
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudio(audioUrl);
      setAudioChunks([]);
    };
  };

  return (
    <div className="Feedback pt-4 container">
      <audio src={audio} controls></audio>
      <form onSubmit={handleSubmit}>
        <div>
          {response.map((item, index) => (
            <div key={index}>
              {/* Render each item here */}
              <p>{item}</p>
              {/* Replace 'propertyName' with the actual property you want to display */}
            </div>
          ))}
        </div>

        <div className="audio-controls">
          {!permission ? (
            <button
              onClick={getMicrophonePermission}
              type="button"
              className="btn"
            >
              Get Microphone
            </button>
          ) : null}
          {permission && recordingStatus === "inactive" ? (
            <button
              onClick={startRecording}
              type="button"
              className="btn btn-success"
            >
              Start Recording
            </button>
          ) : null}
          {recordingStatus === "recording" ? (
            <button
              onClick={stopRecording}
              type="button"
              className="btn btn-danger"
            >
              Stop Recording
            </button>
          ) : null}
        </div>
        <div>
          <textarea name="General" className="flex"></textarea>
        </div>
        <button type="Submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
}

export default FeedbackForm;
