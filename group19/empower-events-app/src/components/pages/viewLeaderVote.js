import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Container, Typography, Grid, FormControlLabel } from '@mui/material';
import Cookies from 'js-cookie';
import { Bar } from 'react-chartjs-2';
import { format, subMonths } from 'date-fns';

const LeaderVote = () => {
    const navigate = useNavigate();
    const [activityLeadersVotes, setActivityLeadersVotes] = useState([]);
    const [selectedDate, setSelectedDate] = useState(new Date());

    useEffect(() => {
        async function fetchActivityLeaderVotes(year, month) {
            try {
                console.log(year, month);
                const csrfToken = Cookies.get('csrftoken');
                const response = await axios.get(`http://localhost:8000/api/leader-vote/results/${year}/${month}`, {
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                });
                if (response.status === 200) {
                    setActivityLeadersVotes(response.data);
                }
            } catch (error) {
                console.error('Error fetching activity leaders:', error);
            }
        }

        const formattedDate = format(selectedDate, 'yyyy/MM');
        const [year, month] = formattedDate.split('/');
        fetchActivityLeaderVotes(year, month);
    }, [selectedDate]);

    const handleDateChange = (date) => {
        setSelectedDate(date);
    };

    const chartData = {
        labels: Object.keys(activityLeadersVotes),
        datasets: [
            {
                label: 'Votes',
                backgroundColor: 'rgba(75,192,192,1)',
                borderColor: 'rgba(0,0,0,1)',
                borderWidth: 2,
                data: Object.values(activityLeadersVotes)
            }
        ]
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Monthly Activity Leader Votes
            </Typography>
            <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} sm={6}>
                    <TextField
                        id="date"
                        label="Select Month"
                        type="month"
                        value={format(selectedDate, 'yyyy-MM')}
                        onChange={(e) => handleDateChange(new Date(e.target.value))}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </Grid>
            </Grid>
            <div style={{ marginTop: '20px' }}>
                {Object.keys(activityLeadersVotes).length > 0 ? (
                    <Bar
                        data={chartData}
                        options={{
                            title: {
                                display: true,
                                text: 'Activity Leader Votes',
                                fontSize: 20
                            },
                            legend: {
                                display: true,
                                position: 'top'
                            },
                            scales: {
                                y: [{
                                    ticks: {
                                        beginAtZero: true,
                                        precision: 0 // This ensures removes decilas from y axis
                                    }
                                }]
                            }
                        }}
                    />
                ) : (
                    <Typography>No data available for the selected month.</Typography>
                )}
            </div>
        </Container>
    );
};

export default LeaderVote;
