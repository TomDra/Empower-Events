import React, { useState,  useEffect} from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Container, Typography, Grid, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import Cookies from 'js-cookie';  // Make sure js-cookie is installed

const AddEvents = () => {
    const navigate = useNavigate();
    const [activityLeaders, setActivityLeaders] = useState([]);
    const [selectedLeader, setSelectedLeader] = useState('');



    const [eventData, setEventData] = useState({
        title: '',
        description: '',
        latitude: '',
        longitude: '',
        age_range_lower: '',
        age_range_higher: '',
        group_title: '',
        compatible_disabilities: '',
        photo_file_path: '',
        time: '',
        activity_leader: ''
    });

    useEffect(() => {
        async function fetchActivityLeaders() {
            try {
                const csrfToken = Cookies.get('csrftoken');
                const response = await axios.get('http://localhost:8000/api/events/add-event', {
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


    const handleChange = (e) => {
        const name = e.target.name;
        const value = e.target.value;

        // Validate if it's a date or time field
        if (name === 'time') {
            const selectedDateTime = new Date(value).getTime();
            const currentDateTime = new Date().getTime();
            if (selectedDateTime <= currentDateTime) {
                // If selected date/time is in the past, set it to the current date/time
                alert('The date has to be in the future.')
                const now = new Date();
                const currentISOString = now.toISOString().slice(0, -8); // Remove milliseconds and timezone offset
                setEventData(prevState => ({
                    ...prevState,
                    [name]: currentISOString // Set to current date/time
                }));
                return;
            }
        }

        setEventData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };


    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        try {
            const csrfToken = Cookies.get('csrftoken');
            const formData = new FormData();
            formData.append('photo', file); // Corrected to use file directly
            const response = await axios.post('http://localhost:8000/api/events/add-event-photo/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': csrfToken
                }
            });
            if (response.status === 201) {
                alert('Photo added successfully!');
                const photo_path_name = response.data.file_name; // corrected to get file_name from response
                // Do something with photo_path_name if needed
                setEventData(prevState => ({
                    ...prevState,
                    photo_file_path: photo_path_name
                }));
            }
        } catch (error) {
            console.error('Error adding photo:', error);
            if (error.response) {
                console.error('Response data:', error.response.data);
            }
            alert('Failed to add the photo. Please check the console for more details.');
        }
        };

     const handleLeaderChange = (e) => {
        const leaderId = e.target.value;
        setSelectedLeader(leaderId);
        setEventData(prevState => ({
            ...prevState,
            activity_leader_id: leaderId
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
                photo_file_path: eventData.photo_file_path ? eventData.photo_file_path : '/defalt'
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
                navigate('/admin/portal')
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
                                    name={'photo'}
                                    key={'photo'}
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
                        <FormControl fullWidth>
                            <InputLabel id="activity-leader-select-label">Activity Leader</InputLabel>
                            <Select
                                labelId="activity-leader-select-label"
                                id="activity-leader-select"
                                value={selectedLeader}
                                onChange={handleLeaderChange}
                            >
                                {activityLeaders.map((leader) => (
                                    <MenuItem key={leader.activity_leader_id} value={leader.activity_leader_id}>
                                        {leader.name}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
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
