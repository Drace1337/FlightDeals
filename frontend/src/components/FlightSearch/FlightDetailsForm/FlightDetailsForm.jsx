import React, { useState } from 'react';
import './FlightDetailsForm.scss';

const FlightDetailsForm = ({ 
  originAirports, 
  destinationAirports,
  onSubmit,
  onBack 
}) => {
  const [details, setDetails] = useState({
    originIata: originAirports[0]?.iataCode || '',
    destinationIata: destinationAirports[0]?.iataCode || '',
    departureDate: '',
    returnDate: '',
    adults: 1
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(details);
  };

  return (
    <form className="flight-details-form" onSubmit={handleSubmit}>
      <h2>Select Flight Details</h2>
      
      <div className="form-group">
        <label>Departure Airport:</label>
        <select
          value={details.originIata}
          onChange={(e) => setDetails({...details, originIata: e.target.value})}
          required
        >
          {originAirports.map(airport => (
            <option key={airport.iataCode} value={airport.iataCode}>
              {airport.name} ({airport.iataCode})
            </option>
          ))}
        </select>
      </div>
      
      <div className="form-group">
        <label>Arrival Airport:</label>
        <select
          value={details.destinationIata}
          onChange={(e) => setDetails({...details, destinationIata: e.target.value})}
          required
        >
          {destinationAirports.map(airport => (
            <option key={airport.iataCode} value={airport.iataCode}>
              {airport.name} ({airport.iataCode})
            </option>
          ))}
        </select>
      </div>

      <div className="dates-row">
        <div className="form-group">
          <label>Departure Date:</label>
          <input
            type="date"
            value={details.departureDate}
            onChange={(e) => setDetails({...details, departureDate: e.target.value})}
            min={new Date().toISOString().split('T')[0]}
            required
          />
        </div>
        
        <div className="form-group">
          <label>Return Date:</label>
          <input
            type="date"
            value={details.returnDate}
            onChange={(e) => setDetails({...details, returnDate: e.target.value})}
            min={details.departureDate || new Date().toISOString().split('T')[0]}
            disabled={!details.departureDate}
          />
        </div>
      </div>
      
    <div className="form-group">
        <label>Passengers:</label>
        <input
            type="number"
            min="1"
            max="10"
            value={details.adults}
            onChange={(e) => setDetails({...details, adults: parseInt(e.target.value) || 1})}
            className="passengers-input"
        />
    </div>
      
      <div className="form-actions">
        <button type="button" className="back-button" onClick={onBack}>
          Back
        </button>
        <button type="submit" className="search-button">
          Search Flights
        </button>
      </div>
    </form>
  );
};

export default FlightDetailsForm;