import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Container, Typography, Grid, FormControlLabel, Checkbox } from '@mui/material';
import Cookies from 'js-cookie';

const LeaderVote = () => {
    const navigate = useNavigate();
    const [activityLeaders, setActivityLeaders] = useState([]);
    const [selectedLeader, setSelectedLeader] = useState('');

    useEffect(() => {
        async function fetchActivityLeaders() {
            try {
                const csrfToken = Cookies.get('csrftoken');
                const response = await axios.get('http://localhost:8000/api/leader-vote/leaders', {
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                });
                if (response.status === 200) {
                    setActivityLeaders(response.data);
                }
            } catch (error) {
                console.error('Error fetching activity leaders:', error);
            }
        }
        fetchActivityLeaders();
    }, []);

    const handleCheckboxChange = (leader) => {
        setSelectedLeader(leader);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedLeader) {
            alert('Please select an activity leader.');
            return;
        }
        const formData = {
                activity_leader_name: selectedLeader.name,
        };

        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await axios.post('http://localhost:8000/api/leader-vote/vote/', formData, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });
            if (response.status === 200) {
                alert('Vote added successfully!');
                navigate('/');
            }
        } catch (error) {
            console.error('Error adding vote:', error);
            if (error.response) {
                console.error('Response data:', error.response.data.error);
                alert(error.response.data.error);
                if (error.response.data.error === "You have already voted this month"){
                    navigate('/')
                }
            }
            else {
                alert('Failed to add the vote. Please check the console for more details.');
            }

        }
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Vote for Activity Leader of the month
            </Typography>
            <form onSubmit={handleSubmit}>
                {activityLeaders.map((leader) => (
                    <FormControlLabel
                        key={leader.name}
                        control={
                            <Checkbox
                                checked={selectedLeader === leader}
                                onChange={() => handleCheckboxChange(leader)}
                                name={leader.name}
                                color="primary"
                            />
                        }
                        label={leader.name}
                    />
                ))}
                <Button type="submit" variant="contained" color="primary">
                    Submit Vote
                </Button>
            </form>
        </Container>
    );
};

export default LeaderVote;
