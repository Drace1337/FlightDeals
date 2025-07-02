import React, { useState } from 'react';
import './SearchForm.scss';

const SearchForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    departureDate: '',
    returnDate: '',
    adults: 1
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.origin) newErrors.origin = 'Origin city is required';
    if (!formData.destination) newErrors.destination = 'Destination city is required';
    if (!formData.departureDate) newErrors.departureDate = 'Departure date is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <h2 className="search-form__title">Find Your Flight</h2>
      
      <div className="search-form__row">
        <div className="search-form__group">
          <label className="search-form__label">From:</label>
          <input
            type="text"
            name="origin"
            value={formData.origin}
            onChange={handleChange}
            className="search-form__input"
            placeholder="City or airport"
          />
          {errors.origin && <p className="search-form__error">{errors.origin}</p>}
        </div>
        
        <div className="search-form__group">
          <label className="search-form__label">To:</label>
          <input
            type="text"
            name="destination"
            value={formData.destination}
            onChange={handleChange}
            className="search-form__input"
            placeholder="City or airport"
          />
          {errors.destination && <p className="search-form__error">{errors.destination}</p>}
        </div>
      </div>

      <div className="search-form__row">
        <div className="search-form__group">
          <label className="search-form__label">Departure:</label>
          <input
            type="date"
            name="departureDate"
            value={formData.departureDate}
            onChange={handleChange}
            className="search-form__input"
            min={new Date().toISOString().split('T')[0]}
          />
          {errors.departureDate && <p className="search-form__error">{errors.departureDate}</p>}
        </div>
        
        <div className="search-form__group">
          <label className="search-form__label">Return (optional):</label>
          <input
            type="date"
            name="returnDate"
            value={formData.returnDate}
            onChange={handleChange}
            className="search-form__input"
            min={formData.departureDate || new Date().toISOString().split('T')[0]}
            disabled={!formData.departureDate}
          />
        </div>
      </div>

      <div className="search-form__group">
        <label className="search-form__label">Passengers:</label>
        <input
          type="number"
          name="adults"
          value={formData.adults}
          onChange={handleChange}
          className="search-form__input"
          min="1"
          max="10"
        />
      </div>

      <button 
        type="submit" 
        className="search-form__button"
        disabled={!formData.origin || !formData.destination || !formData.departureDate}
      >
        Search Flights
      </button>
    </form>
  );
};

export default SearchForm;