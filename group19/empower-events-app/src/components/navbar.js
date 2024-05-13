import React, { useContext } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { UserContext } from '../contexts/userContext';
import axios from 'axios';

const AppNavbar = () => {
  const { isLoggedIn, handleLogout } = useContext(UserContext);
  const navigate = useNavigate();

  const onLogout = async () => {
    try {
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

      if (!csrfToken) {
        console.error('CSRF token not found');
        return;
      }

      await axios.post('http://localhost:8000/api/auth/logout/', {}, {
        headers: {
          'X-CSRFToken': csrfToken, // Include the CSRF token manually
        },
      });
      handleLogout();
      navigate('/login'); // Redirect to login page after logout
    } catch (error) {
      console.error('Error logging out:', error);
      handleLogout();
    }
  };


  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Empower Events</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <NavLink className="nav-link" to="/events/future">Events</NavLink>
            <NavLink className="nav-link" to="/contact-us">Contact Us</NavLink>
            {isLoggedIn ? (
              <>
                <NavLink className="nav-link" to="/events/past">Give Feedback</NavLink>
                <NavLink className="nav-link" to="#" onClick={onLogout}>Logout</NavLink>
              </>
            ) : (
              <>
                <NavLink className="nav-link" to="/login">Login</NavLink>

              </>
            )}
          </Nav>
          <Nav className="ms-auto">
            <NavLink className="nav-link" to="/charity/login">Charity Portal</NavLink>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
