// src/components/HelloWorld.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { speak } from './utils/CheckSpeech'; // Adjust the path based on your actual file structure

export function HelloWorld() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/hello-world/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  const handleSpeak = () => {
    speak(message);
  };

  return (
    <div>
      <h1>Hello, World! (React)</h1>
      <p>{message}</p>
      <button onClick={handleSpeak}>Hear Message</button>
    </div>
  );
}

export default HelloWorld;
