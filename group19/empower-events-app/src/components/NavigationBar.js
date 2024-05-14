// NavigationBar.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import AppNavbar from './navbar';
import CharityAppNavbar from './charityNavbar';

const NavigationBar = ({ isLoggedIn, onLogout }) => {
  const location = useLocation();

  // Check if the current location starts with '/admin'
  const isAdminPage = location.pathname.startsWith('/admin');

  // Conditional rendering of navigation bar based on the isAdminPage flag
  return isAdminPage ? (
    <CharityAppNavbar />
  ) : (
    <AppNavbar isLoggedIn={isLoggedIn} onLogout={onLogout} />
  );
};

export default NavigationBar;
