import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.scss';

const Header = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <header className="header">
      <div className="header__container">
        <Link to="/" className="header__logo">FlightFinder</Link>
        <nav className="header__nav">
          {isLoggedIn ? (
            <>
              <Link to="/profile" className="header__link">Profile</Link>
              <Link to="/history" className="header__link">History</Link>
              <button onClick={handleLogout} className="header__button">Logout</button>
            </>
          ) : (
            <Link to="/auth" className="header__link">Login/Register</Link>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;