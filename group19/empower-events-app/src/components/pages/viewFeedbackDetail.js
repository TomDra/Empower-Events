import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { ArcElement, RadialLinearScale } from 'chart.js';
import { PolarArea } from 'react-chartjs-2';


import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  Title,
  BarElement,
  Tooltip
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  Title,
  BarElement,
  Tooltip
);


ChartJS.register(ArcElement, CategoryScale, RadialLinearScale, Tooltip);

const AdminFeedback = () => {
  const [feedbackCounts, setFeedbackCounts] = useState([]);
  const [responseData, setResponseData] = useState("");
  const [activityFeedback, setActivityFeedback] = useState([]);
  const [leaderFeedback, setLeaderFeedback] = useState([]);
  const [questions, setQuestions] = useState({});
  const { eventId } = useParams();
  const [sentimentData, setSentimentData] = useState({});
  const [questionChartData, setQuestionChartData] = useState(null);

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
            `http://localhost:8000/api/feedback/${eventId}/feedback-questions-details`
          ),
        ]);

        setResponseData(responseOverview.data);
        setActivityFeedback(responseActivity.data.results);
        setLeaderFeedback(responseLeader.data.results);
        setQuestions(responseQuestions.data.questions);

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

        // Prepare data for question chart
        const questionLabels = Object.keys(responseQuestions.data.questions);
        const questionData = questionLabels.map((label) => {
          const { positive, negative } = responseQuestions.data.questions[label];
          return {
            label,
            positive: positive,
            negative: negative
          };
        });

        setQuestionChartData({
          labels: questionLabels,
          datasets: [
            {
              label: "Positive",
              backgroundColor: "rgba(75,192,192,0.4)",
              borderColor: "rgba(75,192,192,1)",
              borderWidth: 1,
              hoverBackgroundColor: "rgba(75,192,192,0.6)",
              hoverBorderColor: "rgba(75,192,192,1)",
              data: questionData.map((data) => data.positive)
            },
            {
              label: "Negative",
              backgroundColor: "rgba(255,99,132,0.4)",
              borderColor: "rgba(255,99,132,1)",
              borderWidth: 1,
              hoverBackgroundColor: "rgba(255,99,132,0.6)",
              hoverBorderColor: "rgba(255,99,132,1)",
              data: questionData.map((data) => data.negative)
            },
            {
              label: "Midpoint",
              backgroundColor: "rgba(255,205,86,0.4)",
              borderColor: "rgba(255,205,86,1)",
              borderWidth: 1,
              hoverBackgroundColor: "rgba(255,205,86,0.6)",
              hoverBorderColor: "rgba(255,205,86,1)",
              data: questionData.map((data) => data.midpoint)
            },
          ]
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    getData();
  }, [eventId]);

  if (
    !responseData ||
    !sentimentData ||
    !activityFeedback ||
    !leaderFeedback ||
    !questions ||
    !feedbackCounts
  ) {
    return <div>Loading...</div>;
  } else {
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
                      <p>{response.leader_feedback_text}</p>
                    </div>
                  ))}
                </div>
              </div>
              <h3>Question responses</h3>
              <div className="card mb-3 text-start">
                <div className="card-body">
                  <Bar
                      data={questionChartData}
                      width={100}

                      height={200}
                      options={{
                        maintainAspectRatio: false,
                        scales: {
                          x: {
                            type: 'category',
                            stacked: false
                          },
                          y: {
                            type: 'linear',
                            stacked: false
                          }
                        }
                      }}
                    />

                </div>
              </div>
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
  }
};

export default AdminFeedback;
