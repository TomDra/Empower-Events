import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const FeedbackForm = ({ match }) => {
  const [eventData, setEventData] = useState({ questions: [] });
  const [responseData, setResponseData] = useState("");
  const [textFeedback, setTextFeedback] = useState("");
  const [radioOptions, setRadioOptions] = useState([]);
  const [permission, setPermission] = useState(false);
  const [stream, setStream] = useState(null);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [audioChunks, setAudioChunks] = useState([]);
  const [audio, setAudio] = useState(null);
  const [base64data, setBase64data] = useState(null);
  const mediaRecorder = useRef(null);
  const { id } = useParams();

  useEffect(() => {
    console.log("id", id);
    const fetchData = async () => {
      try {
        let response;
        response = await axios.get(`http://localhost:8000/api/feedback/${id}/activity-feedback-list`);
        setResponseData(response.data);
        console.log(response.data);
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
    try {
      const reader = new FileReader();
      reader.readAsDataURL(audio);
      reader.onloadend = () => {
        base64data = reader.result.split(",")[1];
      };

      await axios.post(
        `http://http://localhost:8000/api/feedback/${id}/feedback-submission`,
        {
          id: id,
          textFeedback: textFeedback,
          audio: base64data,
          questionAnswers: radioOptions,
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
    const media = new MediaRecorder(stream, { type: "audio/wav" });
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
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      //creates a playable URL from the blob file.
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudio(audioUrl);
      setAudioChunks([]);
    };
  };

  if (!responseData) return <div>Loading...</div>;

  return (
    <div className="Feedback pt-4 container">
      <h1>Feedback for {responseData.description}</h1>
      <form onSubmit={handleSubmit}>
        {eventData.questions.map((question, index) => (
          <div className="row justify-content-center">
            <div className="card mb-3 text-start">
              <h5 className="card-title">{question}</h5>
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
                  class="btn btn-outline-success bi bi-emoji-smile fs-1 "
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
                  class="btn btn-outline-danger bi bi-emoji-frown fs-1"
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
            <audio src={audio} controls></audio>
          </div>
        </div>
        <div className="form-floating">
          <textarea
            name="general-feedback"
            className="form-control"
            id="TextArea"
            style={{ height: "100px" }}
            onChange={(e) => setTextFeedback(e.target.value)}
          ></textarea>
          <label htmlFor="TextArea">Type general feedback here</label>
        </div>
        <button type="Submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
};

export default FeedbackForm;
