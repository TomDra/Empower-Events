import React from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  RadialLinearScale,
  Tooltip,
} from "chart.js";
import { Pie, PolarArea } from "react-chartjs-2";
ChartJS.register(ArcElement, CategoryScale, RadialLinearScale, Tooltip);

const AdminFeedback = () => {
  const [responseData, setResponseData] = useState("");
  const [activityFeedback, setActivityFeedback] = useState("");
  const [leaderFeedback, setLeaderFeedback] = useState("");
  const [questions, setQuestions] = useState("");
  const { id } = useParams();
  const [sentimentData, setSentimentData] = useState({});

  const getData = async () => {
    try {
      let responseOverview = await axios.get(
        `http://localhost:8000/api/feedback/${id}/overview`
      );
      let responseActivity = await axios.get(
        `http://localhost:8000/api/feedback/${id}/activity-feedback-list`
      );
      let responseLeader = await axios.get(
        `http://localhost:8000/api/feedback/${id}/leader-feedback-list`
      );
      let responseQuestions = await axios.get(
        `http://localhost:8000/api/feedback/${id}/feedback-questions-list`
      );
      setResponseData(responseOverview.data);
      setActivityFeedback(responseActivity.data);
      setLeaderFeedback(responseLeader.data);
      setQuestions(responseQuestions.data);
      console.log(responseOverview.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  useEffect(() => {
    getData();
    setSentimentData({
      labels: [
        "Average user sentiment",
        "Average leader sentiment",
        "Average user subjectivity",
        "Average leader subjectivity",
      ],
      datasets: [
        {
          data: [
            responseData.average_user_sentiment,
            responseData.average_leader_sentiment,
            responseData.average_user_sentiment,
            responseData.average_leader_subjectivity,
          ],
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(75, 192, 192)",
            "rgb(255, 205, 86)",
            "rgb(201, 203, 207)",
          ],
        },
      ],
    });
  }, []);

  if (!responseData) return <div>Loading...</div>;

  return (
    <div className="container mt-4">
      <h1>Feedback for </h1>
      <div className="row">
        <div className="col">
          <PolarArea
            data={sentimentData}
            width={300}
            height={300}
            options={{ maintainAspectRatio: false }}
          />
        </div>
      </div>
    </div>
  );
};

export default AdminFeedback;
