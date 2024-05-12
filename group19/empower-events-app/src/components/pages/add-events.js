import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Grid, Box } from '@mui/material';

const AddEvents = () => {
    const [eventData, setEventData] = useState({
        title: '',
        description: '',
        latitude: '',
        longitude: '',
        age_group: '',
        compatible_disabilities: '',
        charity: '',
        photo_file_path: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEventData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/events/', eventData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.status === 201) {
                alert('Event added successfully!');
                setEventData({
                    title: '',
                    description: '',
                    latitude: '',
                    longitude: '',
                    age_group: '',
                    compatible_disabilities: '',
                    charity: '',
                    photo_file_path: ''
                }); // Reset form
            }
        } catch (error) {
            console.error('Error adding event:', error);
            alert('Failed to add the event. Please check the console for more details.');
        }
    };

    return (
        <Container maxWidth="md">
            <Typography variant="h4" component="h1" gutterBottom>
                Add New Event
            </Typography>
            <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label="Title"
                            name="title"
                            value={eventData.title}
                            onChange={handleChange}
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label="Description"
                            name="description"
                            value={eventData.description}
                            onChange={handleChange}
                            required
                            multiline
                            rows={4}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Latitude"
                            name="latitude"
                            value={eventData.latitude}
                            onChange={handleChange}
                            required
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Longitude"
                            name="longitude"
                            value={eventData.longitude}
                            onChange={handleChange}
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label="Age Group ID"
                            name="age_group"
                            value={eventData.age_group}
                            onChange={handleChange}
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label="Compatible Disabilities"
                            name="compatible_disabilities"
                            value={eventData.compatible_disabilities}
                            onChange={handleChange}
                            multiline
                            rows={2}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label="Charity ID"
                            name="charity"
                            value={eventData.charity}
                            onChange={handleChange}
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label="Photo File Path"
                            name="photo_file_path"
                            value={eventData.photo_file_path}
                            onChange={handleChange}
                        />
                    </Grid>
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
