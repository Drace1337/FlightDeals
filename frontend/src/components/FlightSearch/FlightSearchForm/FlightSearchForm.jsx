import React, { useState } from 'react';
import './FlightSearchForm.scss';

const FlightSearchForm = ({ onSubmit }) => {
  const [cities, setCities] = useState({ origin: '', destination: '' });
  const [errors, setErrors] = useState({});

  const isAuthenticated = !!localStorage.getItem('token');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      alert('Please log in to search for flights.');
      return;
    }
    const newErrors = {};
    
    if (!cities.origin.trim()) newErrors.origin = 'Please enter departure city';
    if (!cities.destination.trim()) newErrors.destination = 'Please enter destination city';
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      onSubmit(cities);
    }
  };

  return (
    <form className="flight-search-form" onSubmit={handleSubmit}>
      <h2>Where would you like to fly?</h2>
      {!isAuthenticated && (
        <p className="login-warning">Login in order to search for flights.</p>
      )}
      <div className="form-group">
        <label>From:</label>
        <input
          type="text"
          value={cities.origin}
          onChange={(e) => setCities({...cities, origin: e.target.value})}
          placeholder="Enter departure city"
          className={errors.origin ? 'error' : ''}
          disabled={!isAuthenticated}
        />
        {errors.origin && <span className="error-message">{errors.origin}</span>}
      </div>
      
      <div className="form-group">
        <label>To:</label>
        <input
          type="text"
          value={cities.destination}
          onChange={(e) => setCities({...cities, destination: e.target.value})}
          placeholder="Enter destination city"
          className={errors.destination ? 'error' : ''}
        />
        {errors.destination && <span className="error-message">{errors.destination}</span>}
      </div>
      
      <button type="submit" className="next-button">
        Next
      </button>
    </form>
  );
};

export default FlightSearchForm;