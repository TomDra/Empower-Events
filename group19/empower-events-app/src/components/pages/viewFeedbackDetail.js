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
import { PolarArea } from "react-chartjs-2";
ChartJS.register(ArcElement, CategoryScale, RadialLinearScale, Tooltip);

const AdminFeedback = () => {
  const [counts, setCounts] = useState([{}]);
  const [responseData, setResponseData] = useState("");
  const [activityFeedback, setActivityFeedback] = useState([]);
  const [leaderFeedback, setLeaderFeedback] = useState([]);
  const [questions, setQuestions] = useState([]);
  const { eventId } = useParams();
  const [sentimentData, setSentimentData] = useState({});

  useEffect(() => {
    const getData = async () => {
      try {
        const [
          responseOverview,
          responseActivity,
          responseLeader,
          responseQuestions,
        ] = await Promise.all([
          axios.get(`http://localhost:8000/api/feedback/${eventId}/overview`),
          axios.get(
            `http://localhost:8000/api/feedback/${eventId}/activity-feedback-list`
          ),
          axios.get(
            `http://localhost:8000/api/feedback/${eventId}/leader-feedback-list`
          ),
          axios.get(
            `http://localhost:8000/api/feedback/${eventId}/feedback-questions-list`
          ),
        ]);

        setResponseData(responseOverview.data);
        setActivityFeedback(responseActivity.data.results);
        setLeaderFeedback(responseLeader.data.results);
        setQuestions(responseQuestions.data);

        const sentimentData = {
          labels: [
            "Average user sentiment",
            "Average leader sentiment",
            "Average user subjectivity",
            "Average leader subjectivity",
          ],
          datasets: [
            {
              data: [
                responseOverview.data.average_user_sentiment,
                responseOverview.data.average_leader_sentiment,
                responseOverview.data.average_user_sentiment,
                responseOverview.data.average_leader_subjectivity,
              ],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(75, 192, 192)",
                "rgb(255, 205, 86)",
                "rgb(201, 203, 207)",
              ],
            },
          ],
        };
        setSentimentData(sentimentData);

        const countsData = questions.map((question, index) => {
          const answers = activityFeedback.map(
            (activityFeedback) =>
              JSON.parse(activityFeedback.activity_feedback_question_answers)[
                index
              ]
          );
          const positiveCount = answers.filter(
            (answer) => answer === "positive"
          ).length;
          const negativeCount = answers.filter(
            (answer) => answer === "negative"
          ).length;
          return {
            question: question.question,
            positiveCount,
            negativeCount,
          };
        });
        setCounts(countsData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    getData();
  }, [eventId, counts, sentimentData]);

  
  if (
    !responseData ||
    !sentimentData ||
    !activityFeedback ||
    !leaderFeedback ||
    !questions ||
    !counts
  )

    return <div>Loading...</div>;
  return (
    <div className="container mt-4">
      <h1>Feedback</h1>
      <div className="row">
        <div className="col">
          <PolarArea
            data={sentimentData}
            width={300}
            height={300}
            options={{ maintainAspectRatio: false }}
          />

        </div>
        <div>
          <div className="row justify-content-center">
            <h3>General activity responses</h3>
            <div className="card mb-3 text-start">
              <div className="card-body">
                {activityFeedback.map((response, index) => (
                  <div key={index}>
                    <p>{response.activity_feedback_text}</p>
                  </div>
                ))}
              </div>
            </div>
            <h3>Leader responses</h3>
            <div className="card mb-3 text-start">
              <div className="card-body">
                {leaderFeedback.map((response, index) => (
                  <div key={index}>
                    <p>{response.activity_feedback_text}</p>
                  </div>
                ))}
              </div>
            </div>
            <h3>Question responses</h3>
            {counts.map((response, index) => (
              <div key={index} className="card mb-3 text-start">
                <h5 className="card-title">{response.question}</h5>
                <div className="card-body">
                  <p>Positive: {response.positiveCount}</p>
                  <p>Negative: {response.negativeCount}</p>
                </div>
              </div>
            ))}
            <h3>Audio responses</h3>
            <div className="card mb-3 text-start">
              <div className="card-body d-flex flex-column align-items-center">
                {activityFeedback.map((response, index) => (
                  <div key={index} className="text-center mb-2">
                    {response.activity_feedback_audio ? (
                      <audio
                        src={response.activity_feedback_audio}
                        controls
                        className="mb-2"
                      ></audio>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminFeedback;
