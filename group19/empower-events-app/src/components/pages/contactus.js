import React, { useState } from 'react';
import axios from 'axios';

const ContactUs = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: ''
    });
    const [submitted, setSubmitted] = useState(false);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await axios.post('/api/contact', formData);
            setSubmitted(true);
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    };

    if (submitted) {
        return <p>Thank you for your message! We will get back to you soon.</p>;
    }

    return (
        <div>
            <h1>Contact Us</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Name:
                    <input type="text" name="name" value={formData.name} onChange={handleChange} required />
                </label>
                <label>
                    Email:
                    <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                </label>
                <label>
                    Message:
                    <textarea name="message" value={formData.message} onChange={handleChange} required></textarea>
                </label>
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default ContactUs;
