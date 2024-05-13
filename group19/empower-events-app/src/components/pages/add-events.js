import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Container, Typography, Grid } from '@mui/material';
import Cookies from 'js-cookie';  // Make sure js-cookie is installed

const AddEvents = () => {
    const navigate = useNavigate();
    const [eventData, setEventData] = useState({
        title: '',
        description: '',
        latitude: '',
        longitude: '',
        age_range_lower: '',
        age_range_higher: '',
        group_title: '',
        compatible_disabilities: '',
        photo_file_path: null,
        time: '',
        activity_leader_id: ''
    });

    const handleChange = (e) => {
        const name = e.target.name;
        const value = e.target.value;
        setEventData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };


    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setEventData(prevState => ({
            ...prevState,
            photo_file_path: file
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = {
            activity: {
                title: eventData.title,
                description: eventData.description,
                latitude: parseFloat(eventData.latitude),
                longitude: parseFloat(eventData.longitude),
                age_group: {
                    age_range_lower: parseInt(eventData.age_range_lower),
                    age_range_higher: parseInt(eventData.age_range_higher),
                    group_title: eventData.group_title
                },
                compatible_disabilities: eventData.compatible_disabilities.split(',').map(disability => disability.trim()), // Convert to array of strings
                photo_file_path: eventData.photo_file_path ? eventData.photo_file_path.name : '/defalt'
            },
            time: eventData.time,
            activity_leader_id: parseInt(eventData.activity_leader_id)
        };

        try {
            const csrfToken = Cookies.get('csrftoken');
            console.log(formData)
            const response = await axios.post('http://localhost:8000/api/events/add-event', formData, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });
            if (response.status === 201) {
                alert('Event added successfully!');
                navigate('/admin/home')
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
                        <TextField fullWidth label="Title" name="title"  required
                        value={eventData['title']}
                                    onChange={handleChange}
                                    key={'title'} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Description" name="description" required multiline rows={4}
                                    value={eventData['description']}
                                    onChange={handleChange}
                                    key={'description'} />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField fullWidth label="Latitude" name="latitude"  required
                                    value={eventData['latitude']}
                                    onChange={handleChange}
                                    key={'latitude'} />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField fullWidth label="Longitude" name="longitude" required
                        value={eventData['longitude']}
                                    onChange={handleChange}
                                    key={'longitude'} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Lower Age Range" name="age_range_lower"   required
                        value={eventData['age_range_lower']}
                                    onChange={handleChange}
                                    key={'age_range_lower'} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Higher Age Range" name="age_range_higher"  required
                                    value={eventData['age_range_higher']}
                                    onChange={handleChange}
                                    key={'age_range_higher'} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Group Title" name="group_title"  required
                                    value={eventData['group_title']}
                                    onChange={handleChange}
                                    key={'group_title'} />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Compatible Disabilities" name="compatible_disabilities"
                                    value={eventData['compatible_disabilities']}
                                    onChange={handleChange}
                                    key={'compatible_disabilities'}
                                    helperText="Comma-separated values" />
                    </Grid>
                    <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    type="file"
                                    label="Event Photo"
                                    name={'photo_file_path'}
                                    key={'photo_file_path'}
                                    onChange={handleFileChange}
                                    inputProps={{ accept: 'image/*' }}
                                />



                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Time" type="datetime-local" name="time"  required
                                    value={eventData['time']}
                                    onChange={handleChange}
                                    key={'time'}
                                    helperText="Comma-separated values" />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField fullWidth label="Activity Leader ID" type="number" name="activity_leader_id"  required
                                    value={eventData['activity_leader_id']}
                                    onChange={handleChange}
                                    key={'activity_leader_id'}
                                    helperText="Comma-separated values" />
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
