import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Grid } from '@mui/material';
import Cookies from 'js-cookie';  // Make sure js-cookie is installed

const AddEvents = () => {
    const [eventData, setEventData] = useState({
        title: '',
        description: '',
        latitude: '',
        longitude: '',
        age_group: {
            age_range_lower: '',
            age_range_higher: '',
            group_title: ''
        },
        compatible_disabilities: [],
        photo_file_path: null,
        time: '',
        activity_leader_id: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        if (name === 'photo_file_path') {
            setEventData(prevState => ({
                ...prevState,
                [name]: e.target.files[0]  // Handle file input
            }));
        } else if (name in eventData.age_group) {
            setEventData(prevState => ({
                ...prevState,
                age_group: {
                    ...prevState.age_group,
                    [name]: value
                }
            }));
        } else {
            setEventData(prevState => ({
                ...prevState,
                [name]: value
            }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();

        formData.append('activity', JSON.stringify({
            title: eventData.title,
            description: eventData.description,
            latitude: eventData.latitude,
            longitude: eventData.longitude,
            age_group_id: eventData.age_group_id,
            compatible_disabilities: eventData.compatible_disabilities,
            charity: eventData.charity,
            feedback_questions: eventData.feedback_questions
        }));
        formData.append('photo', eventData.photo);
        formData.append('time', eventData.time);
        formData.append('activity_leader_id', eventData.activity_leader_id);

        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await axios.post('http://localhost:8000/api/events/add-event', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': csrfToken
                }
            });
            if (response.status === 201) {
                alert('Event added successfully!');
                // Reset form
                setEventData({
                    title: '',
                    description: '',
                    latitude: '',
                    longitude: '',
                    age_group: {
                        age_range_lower: '',
                        age_range_higher: '',
                        group_title: ''
                    },
                    compatible_disabilities: [],
                    photo_file_path: null,
                    time: '',
                    activity_leader_id: ''
                });
            }
        } catch (error) {
            console.error('Error adding event:', error);
            if (error.response) {
                console.error('Response data:', error.response.data);
            }
            alert('Failed to add the event. Please check the console for more details.');
        }
    };

    return (
        <Container maxWidth="md">
            <Typography variant="h4" gutterBottom>
                Add New Event
            </Typography>
            <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                    {/* Fields for event data */}
                    <Grid item xs={12}>
                        <TextField fullWidth label="Title" name="title" value={eventData.title} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Description" name="description" value={eventData.description} onChange={handleInputChange} required multiline rows={4} />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField fullWidth label="Latitude" name="latitude" value={eventData.latitude} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField fullWidth label="Longitude" name="longitude" value={eventData.longitude} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Lower Age Range" name="age_range_lower" value={eventData.age_group.age_range_lower} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Higher Age Range" name="age_range_higher" value={eventData.age_group.age_range_higher} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Group Title" name="group_title" value={eventData.age_group.group_title} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Compatible Disabilities" name="compatible_disabilities" value={eventData.compatible_disabilities} onChange={handleInputChange} helperText="Comma-separated values" />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth type="file" label="Event Photo" name="photo_file_path" onChange={handleInputChange} inputProps={{ accept: 'image/*' }} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Time" type="datetime-local" name="time" value={eventData.time} onChange={handleInputChange} required />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Activity Leader ID" type="number" name="activity_leader_id" value={eventData.activity_leader_id} onChange={handleInputChange} required />
                    </Grid>
                    {/* Submit button */}
                    <Grid item xs={12}>
                        <Button type="submit" variant="contained" color="primary">
                            Add Event
                        </Button>
                    </Grid>
                </Grid>
            </form>
        </Container>
    );
};

export default AddEvents;
