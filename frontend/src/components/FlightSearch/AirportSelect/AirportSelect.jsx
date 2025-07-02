import React, { useEffect, useState } from 'react';
import './AirportSelect.scss';

const AirportSelect = ({ city, onSelect, className }) => {
  const [airports, setAirports] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!city) return;
    
    setLoading(true);
    fetch(`/search/iata?city=${encodeURIComponent(city)}`)
      .then(res => res.json())
      .then(data => {
        setAirports(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [city]);

  return (
    <div className={`airport-select ${className}`}>
      {loading ? (
        <div className="airport-select__loading">Loading airports...</div>
      ) : (
        <select
          className="airport-select__dropdown"
          onChange={(e) => onSelect(e.target.value)}
          disabled={!airports.length}
        >
          <option value="">Select airport in {city}</option>
          {airports.map(airport => (
            <option key={airport.iataCode} value={airport.iataCode}>
              {airport.name} ({airport.iataCode})
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default AirportSelect;