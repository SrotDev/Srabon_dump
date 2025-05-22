import React from 'react';
import logo from '../assets/images/logo.png'; // adjust path if needed
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar__container">
        <div className="navbar__logo">
          <NavLink to="/"><img src={logo} alt="Srabon Logo" style={{ height: '50px' }} /></NavLink>
        </div>
        <ul className="navbar__links">
          <li><NavLink to="/functionalities" className={({ isActive }) => isActive ? "active" : ""}>Home</NavLink></li>
          <li><NavLink to="/courses" className={({ isActive }) => isActive ? "active" : ""}>Courses</NavLink></li>
          <li><NavLink to="/explore" className={({ isActive }) => isActive ? "active" : ""}>Explore</NavLink></li>
          <li><NavLink to="/chat" className={({ isActive }) => isActive ? "active" : ""}>Chat</NavLink></li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
