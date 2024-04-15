// Importing necessary modules and components from React and Axios
import React, { useState } from 'react';
import axios from 'axios';

// Setting Axios defaults for CSRF protection and enabling credentials
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

// Defining the SignUp component
const SignUp = () => {
    // Initializing state variables using the useState hook
    const [email, setEmail] = useState(''); // To store the entered email
    const [password, setPassword] = useState(''); // To store the entered password
    const [confirmPassword, setConfirmPassword] = useState(''); // To store the confirmed password
    const [username, setUsername] = useState(''); // To store the entered username
    const [errorMessage, setErrorMessage] = useState(''); // To store error messages during sign-up

    // Handling form submission
    const handleSubmit = async (e) => {
        e.preventDefault(); // Preventing default form submission behavior
        
        // Checking if passwords match
        if (password !== confirmPassword) {
            setErrorMessage('Passwords do not match.');
            return;
        }
        
        try {
            // Sending a POST request to the backend API for sign-up
            const response = await axios.post('http://localhost:8000/api/auth/register/', {
                username, // Sending username entered by the user
                email, // Sending email entered by the user
                password, // Sending password entered by the user
            });
    
            console.log('Sign-up successful:', response.data); // Logging successful sign-up response
            // Redirecting user to the login page or automatically logging them in after signing up
        } catch (error) {
            // Error handling
            const detailedError = error.response ? (error.response.data.detail || JSON.stringify(error.response.data)) : error.message;
            console.error('Sign-up failed:', detailedError); // Logging error message if sign-up fails
            setErrorMessage('An error occurred during sign-up: ' + detailedError); // Setting error message state
        }
    };

    // Rendering the sign-up form
    return (
        <div>
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)} // Handling username input change
                    />
                </div>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)} // Handling email input change
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)} // Handling password input change
                    />
                </div>
                <div>
                    <label htmlFor="confirmPassword">Confirm Password:</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)} // Handling confirm password input change
                    />
                </div>
                {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>} {/* Displaying error message if exists */}
                <button type="submit">Sign Up</button> {/* Submit button */}
            </form>
            <a href="/login">Login instead</a>
        </div>
    );
}

// Exporting the SignUp component as the default export
export default SignUp;
