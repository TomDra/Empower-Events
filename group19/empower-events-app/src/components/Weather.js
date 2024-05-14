// src/components/WeatherNotification.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const WeatherNotification = ({ lat, lon }) => {
  const [previousWeather, setPreviousWeather] = useState(null);

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/weather/getWeather/', {
          params: { lat, lon },
        });

        if (response.status === 200) {
          const { main, weather } = response.data;
          const temperature = main.temp - 273.15; // Convert from Kelvin to Celsius
          const weatherDescription = weather[0].description;

          const newWeather = {
            temperature: parseFloat(temperature.toFixed(2)), // round to 2 decimal places
            description: weatherDescription,
          };

          if (!previousWeather || 
              (Math.abs(previousWeather.temperature - newWeather.temperature) >= 0.01 || 
              previousWeather.description !== newWeather.description)) {
            toast.info(`Current temperature: ${newWeather.temperature}°C. Weather: ${newWeather.description}`);
            setPreviousWeather(newWeather);
          }
        } else {
          toast.error('Failed to fetch weather data');
        }
      } catch (error) {
        console.error('Error fetching weather data:', error);
        toast.error('Error fetching weather data');
      }
    };

    // Fetch weather data periodically
    const intervalId = setInterval(fetchWeather, 60000); // Fetch every 60 seconds

    // Initial fetch
    fetchWeather();

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, [lat, lon, previousWeather]);

  return <ToastContainer />;
};

export default WeatherNotification;
