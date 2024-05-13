import React, { useState } from 'react';
import axios from 'axios';

const ContactUs = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: ''
    });
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/api/contact/', formData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.status === 200) {
                setSubmitted(true);
                setFormData({ name: '', email: '', message: '' }); // Reset form
            } else {
                console.error('Server responded with non-200 status:', response.status);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            alert('Failed to send message. Please try again.');
        }
        setLoading(false);
    };

    if (submitted) {
        return <div className="alert alert-success">Thank you for your message! We will get back to you soon.</div>;
    }

    if (loading) {
        return <div>Loading...</div>; // Display loading indicator while sending request
    }

    return (
        <div className="container mt-5">
            <h1>Contact Us</h1>
            <form onSubmit={handleSubmit} className="mt-3">
                <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name:</label>
                    <input type="text" className="form-control" id="name" name="name" value={formData.name} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email:</label>
                    <input type="email" className="form-control" id="email" name="email" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label htmlFor="message" className="form-label">Message:</label>
                    <textarea className="form-control" id="message" name="message" rows="4" value={formData.message} onChange={handleChange} required />
                </div>
                <button type="submit" className="btn btn-primary" disabled={loading}>Send</button>
            </form>
        </div>
    );
};

export default ContactUs;
